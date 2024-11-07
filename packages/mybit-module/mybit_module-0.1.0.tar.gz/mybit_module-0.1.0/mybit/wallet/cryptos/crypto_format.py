import hashlib

from coincurve import verify_signature as _vs

from mybit.bit_modules.base58 import b58decode_check, b58encode_check
from mybit.bit_modules.crypto import ripemd160_sha256, sha256
from mybit.bit_modules.curve import x_to_y
from mybit.bit_modules.utils import int_to_unknown_bytes, script_push
from mybit.transactions.base32 import Base32

class CryptoFormat:
    """Clase común para operaciones criptográficas, con soporte para múltiples criptomonedas."""

    def __init__(self, constants):
        # Cargamos las constantes desde la configuración pasada
        self.constants = constants
        self.base32 = Base32(constants)


    def verify_sig(self, signature, data, public_key):
        """Verifies some data was signed by the owner of a public key.

        :param signature: The signature to verify.
        :type signature: ``bytes``
        :param data: The data that was supposedly signed.
        :type data: ``bytes``
        :param public_key: The public key.
        :type public_key: ``bytes``
        :returns: ``True`` if all checks pass, ``False`` otherwise.
        """
        return _vs(signature, data, public_key)


    def address_to_public_key_hash(self, address):
        # Raise ValueError if we cannot identify the address.
        self.get_version(address)
        return b58decode_check(address)[1:]


    def get_version(self, address):
        # Intenta decodificar usando Bech32
        version, _ = self.base32.bech32_decode(address)

        # Si no es Bech32, intenta decodificar usando Base58
        if version is None:
            version = b58decode_check(address)[:1]

        # Verifica si la versión corresponde a mainnet
        if version in (self.constants.MAIN_PUBKEY_HASH, self.constants.MAIN_SCRIPT_HASH) or version in self.constants.BECH32_MAIN_VERSION_SET:
            return 'main'

        # Verifica si la versión corresponde a testnet
        elif version in (self.constants.TEST_PUBKEY_HASH, self.constants.TEST_SCRIPT_HASH) or version in self.constants.BECH32_TEST_VERSION_SET:
            return 'test'
        
        # Si no es ninguno de los anteriores, lanzamos una excepción
        else:
            raise ValueError(f'{address} no corresponde a una dirección de mainnet ni testnet.')

    def validate_address(self, address: str, address_version: str) -> bool:
        """
        Verifica si una dirección es válida, decodificándola en Base58 o Bech32
        y asegurando que la versión coincida con los prefijos aceptados por la red.

        :param address: La dirección de la wallet a validar.
        :type address: str
        :param address_version: La versión de la dirección (main o test).
        :type address_version: str
        :returns: True si la dirección es válida, False en caso contrario.
        :rtype: bool
        """
        try:
            # Intenta decodificar usando Bech32
            version, _ = self.base32.bech32_decode(address)

            # Si no es Bech32, intenta decodificar usando Base58
            if version is None:
                version = b58decode_check(address)[:1]

            # Mapa de versiones según el tipo de red
            version_map = {
                'main': (self.constants.MAIN_PUBKEY_HASH, self.constants.MAIN_SCRIPT_HASH, self.constants.BECH32_MAIN_VERSION_SET),
                'test': (self.constants.TEST_PUBKEY_HASH, self.constants.TEST_SCRIPT_HASH, self.constants.BECH32_TEST_VERSION_SET)
            }

            # Verificar si la versión es válida según la red (main o test)
            if not address_version in version_map:
                return False
            
            pubkey_hash, script_hash, bech32_set = version_map[address_version]
            if version in (pubkey_hash, script_hash) or version in bech32_set:
                return True

        except ValueError:
            pass  # Si ocurre un error de decodificación, la dirección no es válida

        return False  # Dirección no válida si no coincide con ninguna condición

    def bytes_to_wif(self, private_key, version='main', compressed=False):
        if version == 'test':
            prefix = self.constants.TEST_PRIVATE_KEY
        else:
            prefix = self.constants.MAIN_PRIVATE_KEY

        if compressed:
            suffix = self.constants.PRIVATE_KEY_COMPRESSED_PUBKEY
        else:
            suffix = b''

        private_key = prefix + private_key + suffix

        return b58encode_check(private_key)


    def wif_to_bytes(self, wif):
        private_key = b58decode_check(wif)
        version = private_key[:1]

        if version == self.constants.MAIN_PRIVATE_KEY:
            version = 'main'

        elif version == self.constants.TEST_PRIVATE_KEY:
            version = 'test'

        else:
            raise ValueError('{} does not correspond to a mainnet nor testnet address.'.format(version))

        # Remove version byte and, if present, compression flag.
        if len(private_key) == 34 and private_key[-1] == 1:
            private_key, compressed = private_key[1:-1], True
        else:
            private_key, compressed = private_key[1:], False

        return private_key, compressed, version

    def wif_checksum_check(self, wif):
        try:
            decoded = b58decode_check(wif)
        except ValueError:
            return False

        if decoded[:1] in (self.constants.MAIN_PRIVATE_KEY, self.constants.TEST_PRIVATE_KEY):
            return True

        return False


    def public_key_to_address(self, public_key, version='main'):
        if version == 'test':
            version = self.constants.TEST_PUBKEY_HASH
        else:
            version = self.constants.MAIN_PUBKEY_HASH

        length = len(public_key)

        if length not in (33, 65):
            raise ValueError('{} is an invalid length for a public key.'.format(length))

        return b58encode_check(version + ripemd160_sha256(public_key))


    def public_key_to_segwit_address(self, public_key, version='main'):
        if not self.constants.SUPPORTS_BECH32:
            return None
        
        if version == 'test':
            version = self.constants.TEST_SCRIPT_HASH
        else:
            version = self.constants.MAIN_SCRIPT_HASH

        length = len(public_key)

        if length != 33:
            raise ValueError(
                '{} is an invalid length for a public key. Segwit only uses compressed public keys'.format(length)
            )

        return b58encode_check(version + ripemd160_sha256(b'\x00\x14' + ripemd160_sha256(public_key)))


    def public_key_to_p2wpkh_address(self, public_key: bytes, version='main') -> str:
        """Convierte una clave pública en una dirección Bech32 (P2WPKH)."""
        if not self.constants.SUPPORTS_BECH32:
            return None
        
        # Realiza el hash sha256 y luego el ripemd160
        sha256_hash = hashlib.sha256(public_key).digest()
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
        
        # El Human Readable Part (hrp) es "bc" para mainnet y "tb" para testnet
        hrp = self.constants.BECH32_MAIN_VERSION_SET[0] if version == 'main' else self.constants.BECH32_TEST_VERSION_SET[0]
        
        # Convierte el hash ripemd160 a formato de 5 bits
        data = self.base32.convertbits(ripemd160_hash, 8, 5)
        
        # Codificar en Bech32 (BIP173) usando el testigo de versión 0 (P2WPKH)
        return self.base32.bech32_encode(hrp, [0] + data)


    def multisig_to_redeemscript(self, public_keys, m):
        if m > len(public_keys):
            raise ValueError('Required signatures cannot be more than the total number of public keys.')

        redeemscript = int_to_unknown_bytes(m + 80)

        for key in public_keys:
            length = len(key)

            if length not in (33, 65):
                raise ValueError('At least one of the provided public keys is of invalid length {}.'.format(length))

            redeemscript += script_push(length) + key

        redeemscript += (
            int_to_unknown_bytes(len(public_keys) + 80) + b'\xae'
        )  # Only works for n = len(public_keys) < 17. OK due to P2SH script-length limitation.

        if len(redeemscript) > 520:
            raise ValueError('The redeemScript exceeds the allowed 520-byte limitation with the number of public keys.')

        return redeemscript


    def multisig_to_address(self, public_keys, m, version='main'):
        if version == 'test':
            version = self.constants.TEST_SCRIPT_HASH
        else:
            version = self.constants.MAIN_SCRIPT_HASH

        return b58encode_check(version + ripemd160_sha256(self.multisig_to_redeemscript(public_keys, m)))


    def multisig_to_segwit_address(self, public_keys, m, version='main'):
        if version == 'test':
            version = self.constants.TEST_SCRIPT_HASH
        else:
            version = self.constants.MAIN_SCRIPT_HASH

        return b58encode_check(version + ripemd160_sha256(b'\x00\x20' + sha256(self.multisig_to_redeemscript(public_keys, m))))


    def segwit_scriptpubkey(self, witver, witprog):
        """Construct a Segwit scriptPubKey for a given witness program."""
        return bytes([witver + 0x50 if witver else 0, len(witprog)] + witprog)


    def public_key_to_coords(self, public_key):
        length = len(public_key)

        if length == 33:
            flag, x = int.from_bytes(public_key[:1], 'big'), int.from_bytes(public_key[1:], 'big')
            y = x_to_y(x, flag & 1)
        elif length == 65:
            x, y = int.from_bytes(public_key[1:33], 'big'), int.from_bytes(public_key[33:], 'big')
        else:
            raise ValueError('{} is an invalid length for a public key.'.format(length))

        return x, y


    def coords_to_public_key(self, x, y, compressed=True):
        if compressed:
            y = self.constants.PUBLIC_KEY_COMPRESSED_ODD_Y if y & 1 else self.constants.PUBLIC_KEY_COMPRESSED_EVEN_Y
            return y + x.to_bytes(32, 'big')

        return self.constants.PUBLIC_KEY_UNCOMPRESSED + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')


    def point_to_public_key(self, point, compressed=True):
        return self.coords_to_public_key(point.x, point.y, compressed)
    

    def address_to_scriptpubkey(self, address):
        # Intentar decodificar la dirección como Base58 (P2PKH o P2SH)
        try:
            version = b58decode_check(address)[:1]
        except ValueError:
            # Si la decodificación Base58 falla, intentamos con Bech32 (SegWit P2WPKH o P2WSH)
            witver, witprog = self.base32.decode(address)
            # Llamar a la función segwit_scriptpubkey para generar el script
            return self.segwit_scriptpubkey(witver, witprog)
        
        # Si la dirección es P2PKH
        if version == self.constants.MAIN_PUBKEY_HASH or version == self.constants.TEST_PUBKEY_HASH:
            return (self.constants.OP_DUP + self.constants.OP_HASH160 + 
                    self.constants.OP_PUSH_20 + self.address_to_public_key_hash(address) + 
                    self.constants.OP_EQUALVERIFY + self.constants.OP_CHECKSIG)
        
        # Si la dirección es P2SH
        elif version == self.constants.MAIN_SCRIPT_HASH or version == self.constants.TEST_SCRIPT_HASH:
            return (self.constants.OP_HASH160 + self.constants.OP_PUSH_20 + 
                    self.address_to_public_key_hash(address) + self.constants.OP_EQUAL)

        # Si no coincide con ninguna, lanzar un error
        raise ValueError("No se reconoce el tipo de dirección")