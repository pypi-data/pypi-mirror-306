import hashlib

from mybit.bit_modules.base58 import b58decode_check
from mybit.transactions.base32 import Base32

class ScriptHashConverter:
    def __init__(self, constants):
        self.address = None
        self.constants = constants
        self.base32 = Base32(constants)
        self._scripthash = None
        self._pubkey_hash = None
    
    def set_address(self, address):
        self.address = address

    @property
    def scripthash(self):
        if self._scripthash is None:
            self._scripthash = self.get_scripthash(self.address)

        return self._scripthash
    
    @property
    def pubkey_hash(self):
        if self._pubkey_hash is None:
            self._pubkey_hash = self.get_pubkey_hash(self.address)
            
        return self._pubkey_hash

    # Obtener el PubKeyHash (P2PKH, P2SH, P2WPKH, P2WSH)
    def get_pubkey_hash(self, address):
        # Intentar decodificar como dirección Base58 (P2PKH o P2SH)
        try:
            decoded = b58decode_check(address)
        except ValueError:
            # Si falla, intentar como Bech32 (P2WPKH o P2WSH)
            return self.get_bech32_pubkey_hash(address)

        if len(decoded) != 21:
            raise ValueError("Dirección Base58 no válida")

        prefix = decoded[0]
        pubkey_hash = decoded[1:]

        # Verificar si es P2PKH
        if prefix == self.constants.MAIN_PUBKEY_HASH[0] or prefix == self.constants.TEST_PUBKEY_HASH[0]:
            return pubkey_hash.hex()

        # Verificar si es P2SH
        if prefix == self.constants.MAIN_SCRIPT_HASH[0] or prefix == self.constants.TEST_SCRIPT_HASH[0]:
            return pubkey_hash.hex()

        raise ValueError("Prefijo de dirección Base58 no reconocido")

    # Obtener el PubKeyHash para direcciones Bech32 (P2WPKH, P2WSH)
    def get_bech32_pubkey_hash(self, bech32_address):
        hrp, data = self.base32.bech32_decode(bech32_address)
        decoded = self.base32.convertbits(data[1:], 5, 8, False)

        if len(decoded) == 20:  # P2WPKH
            return bytes(decoded).hex()
        elif len(decoded) == 32:  # P2WSH
            return bytes(decoded).hex()
        else:
            raise ValueError("Longitud del hash no válida para un witness program")

    # P2PKH (Litecoin y Bitcoin)
    def p2pkh_to_scripthash(self, decoded):
        # Obtener el PubKeyHash (20 bytes)
        pubkey_hash = decoded[1:]

        # Crear scriptPubKey usando constantes
        script_pubkey = (
            self.constants.OP_DUP +
            self.constants.OP_HASH160 +
            self.constants.OP_PUSH_20 +  # Ya es un objeto bytes, no es necesario envolverlo
            pubkey_hash +
            self.constants.OP_EQUALVERIFY +
            self.constants.OP_CHECKSIG
        )

        # Calcular el script hash (SHA256(scriptPubKey)) y revertir el orden de bytes
        scripthash = hashlib.sha256(script_pubkey).digest()[::-1].hex()
        return scripthash

    # P2SH (Litecoin y Bitcoin)
    def p2sh_to_scripthash(self, decoded):
        # Obtener el RedeemScriptHash (20 bytes)
        redeem_script_hash = decoded[1:]

        # Crear scriptPubKey: OP_HASH160 + redeem script hash + OP_EQUAL
        script_pubkey = (
            self.constants.OP_HASH160 + 
            self.constants.OP_PUSH_20 + 
            redeem_script_hash + 
            self.constants.OP_EQUAL
        )

        # Calcular el script hash (SHA256(scriptPubKey)) y revertir el orden de bytes
        scripthash = hashlib.sha256(script_pubkey).digest()[::-1].hex()
        return scripthash

    # Bech32 (P2WPKH y P2WSH)
    def bech32_to_scripthash(self, bech32_address):
        hrp, data = self.base32.bech32_decode(bech32_address)
        decoded = self.base32.convertbits(data[1:], 5, 8, False)

        if len(decoded) == 20:  # P2WPKH
            script_pubkey = self.constants.OP_0 + self.constants.OP_PUSH_20 + bytes(decoded)
        elif len(decoded) == 32:  # P2WSH
            script_pubkey = self.constants.OP_0 + self.constants.OP_PUSH_32 + bytes(decoded)
        else:
            raise ValueError("Longitud del hash no válida para un witness program")

        scripthash = hashlib.sha256(script_pubkey).digest()[::-1].hex()
        return scripthash

    # P2WPKH-in-P2SH
    def p2wpkh_in_p2sh_to_scripthash(self, decoded):
        return self.p2sh_to_scripthash(decoded)

    # P2WSH-in-P2SH
    def p2wsh_in_p2sh_to_scripthash(self, decoded):
        return self.p2sh_to_scripthash(decoded)

    def get_scripthash(self, address):
        # Intentar decodificar como dirección Base58 (P2PKH o P2SH)
        try:
            decoded = b58decode_check(address)
        except ValueError:
            return self.bech32_to_scripthash(address)

        if len(decoded) != 21:
            raise ValueError("Dirección Base58 no válida")

        prefix = decoded[0]

        # Asegurarse de que las constantes de prefijo estén comparadas como enteros
        if prefix == self.constants.MAIN_PUBKEY_HASH[0] or prefix == self.constants.TEST_PUBKEY_HASH[0]:
            return self.p2pkh_to_scripthash(decoded)

        # P2SH: Comparar los prefijos P2SH correctamente
        if prefix == self.constants.MAIN_SCRIPT_HASH[0] or prefix == self.constants.TEST_SCRIPT_HASH[0]:
            redeem_script_hash = decoded[1:]

            if len(redeem_script_hash) != 20 and len(redeem_script_hash) != 32:
                raise ValueError("Longitud de redeem script no válida")

            # Usar las constantes para P2WPKH y P2WSH
            if redeem_script_hash[:2] == self.constants.OP_0 + self.constants.OP_PUSH_20:
                return self.p2wpkh_in_p2sh_to_scripthash(decoded)

            if redeem_script_hash[:2] == self.constants.OP_0 + self.constants.OP_PUSH_32:
                return self.p2wsh_in_p2sh_to_scripthash(decoded)

            return self.p2sh_to_scripthash(decoded)

        raise ValueError("Prefijo de dirección Base58 no reconocido")