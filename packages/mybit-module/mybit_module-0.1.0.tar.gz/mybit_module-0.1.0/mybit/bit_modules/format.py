import hashlib

from coincurve import verify_signature as _vs

from mybit.bit_modules.base58 import b58decode_check, b58encode_check
from mybit.bit_modules.crypto import ripemd160_sha256, sha256
from mybit.bit_modules.curve import x_to_y

from mybit.bit_modules.utils import int_to_unknown_bytes, hex_to_bytes, script_push
from mybit.bit_modules.base32 import bech32_decode, bech32_encode, convertbits
from mybit.bit_modules.constants import (
    BECH32_MAIN_VERSION_SET,
    BECH32_TEST_VERSION_SET,
    MAIN_PUBKEY_HASH,
    MAIN_SCRIPT_HASH,
    MAIN_PRIVATE_KEY,
    TEST_PUBKEY_HASH,
    TEST_SCRIPT_HASH,
    TEST_PRIVATE_KEY,
    PUBLIC_KEY_UNCOMPRESSED,
    PUBLIC_KEY_COMPRESSED_EVEN_Y,
    PUBLIC_KEY_COMPRESSED_ODD_Y,
    PRIVATE_KEY_COMPRESSED_PUBKEY,
)

# Mapeo de prefijos de criptomonedas según la red (mainnet/testnet)
# BECH32_PREFIXES = {
#     'bitcoin': {'mainnet': BECH32_MAIN_VERSION_SET[0], 'testnet': BECH32_TEST_VERSION_SET[0]},
#     'litecoin': {'mainnet': 'ltc', 'testnet': 'tltc'},
#     # Puedes agregar otras criptos aquí
# }


def verify_sig(signature, data, public_key):
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


def address_to_public_key_hash(address):
    # Raise ValueError if we cannot identify the address.
    get_version(address)
    return b58decode_check(address)[1:]


def get_version(address):
    version, _ = bech32_decode(address)

    if version is None:
        version = b58decode_check(address)[:1]
    if version in (MAIN_PUBKEY_HASH, MAIN_SCRIPT_HASH) or version in BECH32_MAIN_VERSION_SET:
        return 'main'
    elif version in (TEST_PUBKEY_HASH, TEST_SCRIPT_HASH) or version in BECH32_TEST_VERSION_SET:
        return 'test'
    else:
        raise ValueError('{} does not correspond to a mainnet nor testnet address.'.format(version))


def bytes_to_wif(private_key, version='main', compressed=False):
    if version == 'test':
        prefix = TEST_PRIVATE_KEY
    else:
        prefix = MAIN_PRIVATE_KEY

    if compressed:
        suffix = PRIVATE_KEY_COMPRESSED_PUBKEY
    else:
        suffix = b''

    private_key = prefix + private_key + suffix

    return b58encode_check(private_key)


def wif_to_bytes(wif):
    private_key = b58decode_check(wif)
    version = private_key[:1]

    if version == MAIN_PRIVATE_KEY:
        version = 'main'
    elif version == TEST_PRIVATE_KEY:
        version = 'test'
    else:
        raise ValueError('{} does not correspond to a mainnet nor testnet address.'.format(version))

    # Remove version byte and, if present, compression flag.
    if len(wif) == 52 and private_key[-1] == 1:
        private_key, compressed = private_key[1:-1], True
    else:
        private_key, compressed = private_key[1:], False

    return private_key, compressed, version


def wif_checksum_check(wif):
    try:
        decoded = b58decode_check(wif)
    except ValueError:
        return False

    if decoded[:1] in (MAIN_PRIVATE_KEY, TEST_PRIVATE_KEY):
        return True

    return False


def public_key_to_address(public_key, version='main'):
    if version == 'test':
        version = TEST_PUBKEY_HASH
    else:
        version = MAIN_PUBKEY_HASH

    length = len(public_key)

    if length not in (33, 65):
        raise ValueError('{} is an invalid length for a public key.'.format(length))

    return b58encode_check(version + ripemd160_sha256(public_key))


def public_key_to_segwit_address(public_key, version='main'):
    if version == 'test':
        version = TEST_SCRIPT_HASH
    else:
        version = MAIN_SCRIPT_HASH

    length = len(public_key)

    if length != 33:
        raise ValueError(
            '{} is an invalid length for a public key. Segwit only uses compressed public keys'.format(length)
        )

    return b58encode_check(version + ripemd160_sha256(b'\x00\x14' + ripemd160_sha256(public_key)))

def public_key_to_p2wpkh_address(public_key: bytes, version='main') -> str:
    """Convierte una clave pública en una dirección Bech32 (P2WPKH)."""
    # Convierte la clave pública de hexadecimal a bytes
    # pubkey = bytes.fromhex(pubkey_hex)
    
    # Realiza el hash sha256 y luego el ripemd160
    sha256_hash = hashlib.sha256(public_key).digest()
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
    
    # El Human Readable Part (hrp) es "bc" para mainnet y "tb" para testnet
    hrp = BECH32_MAIN_VERSION_SET[0] if version == 'main' else BECH32_TEST_VERSION_SET[0]
    
    # Convierte el hash ripemd160 a formato de 5 bits
    data = convertbits(ripemd160_hash, 8, 5)
    
    # Codificar en Bech32 (BIP173) usando el testigo de versión 0 (P2WPKH)
    return bech32_encode(hrp, [0] + data)


def multisig_to_redeemscript(public_keys, m):
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


def multisig_to_address(public_keys, m, version='main'):
    if version == 'test':
        version = TEST_SCRIPT_HASH
    else:
        version = MAIN_SCRIPT_HASH

    return b58encode_check(version + ripemd160_sha256(multisig_to_redeemscript(public_keys, m)))


def multisig_to_segwit_address(public_keys, m, version='main'):
    if version == 'test':
        version = TEST_SCRIPT_HASH
    else:
        version = MAIN_SCRIPT_HASH

    return b58encode_check(version + ripemd160_sha256(b'\x00\x20' + sha256(multisig_to_redeemscript(public_keys, m))))


def segwit_scriptpubkey(witver, witprog):
    """Construct a Segwit scriptPubKey for a given witness program."""
    return bytes([witver + 0x50 if witver else 0, len(witprog)] + witprog)


def public_key_to_coords(public_key):
    length = len(public_key)

    if length == 33:
        flag, x = int.from_bytes(public_key[:1], 'big'), int.from_bytes(public_key[1:], 'big')
        y = x_to_y(x, flag & 1)
    elif length == 65:
        x, y = int.from_bytes(public_key[1:33], 'big'), int.from_bytes(public_key[33:], 'big')
    else:
        raise ValueError('{} is an invalid length for a public key.'.format(length))

    return x, y


def coords_to_public_key(x, y, compressed=True):
    if compressed:
        y = PUBLIC_KEY_COMPRESSED_ODD_Y if y & 1 else PUBLIC_KEY_COMPRESSED_EVEN_Y
        return y + x.to_bytes(32, 'big')

    return PUBLIC_KEY_UNCOMPRESSED + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')


def point_to_public_key(point, compressed=True):
    return coords_to_public_key(point.x, point.y, compressed)
