# base_constants.py
class BaseConstants:
    SUPPORTS_BECH32 = False
    SUPPORTS_SEGWIT = False

    VERSION_1 = 0x01 .to_bytes(4, byteorder='little')
    VERSION_2 = 0x02 .to_bytes(4, byteorder='little')
    MARKER = b'\x00'
    FLAG = b'\x01'
    SEQUENCE = 0xFFFFFFFF .to_bytes(4, byteorder='little')
    LOCK_TIME = 0x00 .to_bytes(4, byteorder='little')
    HASH_TYPE = 0x01 .to_bytes(4, byteorder='little')

    # Scripts:
    OP_0 = b'\x00'
    OP_CHECKLOCKTIMEVERIFY = b'\xb1'
    OP_CHECKSIG = b'\xac'
    OP_CHECKMULTISIG = b'\xae'
    OP_DUP = b'v'
    OP_EQUALVERIFY = b'\x88'
    OP_HASH160 = b'\xa9'
    OP_PUSH_20 = b'\x14'
    OP_PUSH_32 = b'\x20'
    OP_RETURN = b'\x6a'
    OP_EQUAL = b'\x87'

    MESSAGE_LIMIT = 80
    # Address formats:
    BECH32_VERSION_SET = ('bc', 'tb', 'bcrt')
    BECH32_MAIN_VERSION_SET = BECH32_VERSION_SET[:1]
    BECH32_TEST_VERSION_SET = BECH32_VERSION_SET[1:]
    MAIN_PUBKEY_HASH = b'\x00'
    MAIN_SCRIPT_HASH = b'\x05'
    TEST_PUBKEY_HASH = b'\x6f'
    TEST_SCRIPT_HASH = b'\xc4'

    # Keys:
    MAIN_PRIVATE_KEY = b'\x80'
    MAIN_BIP32_PUBKEY = b'\x04\x88\xb2\x1e'
    MAIN_BIP32_PRIVKEY = b'\x04\x88\xad\xe4'
    TEST_PRIVATE_KEY = b'\xef'
    TEST_BIP32_PUBKEY = b'\x045\x87\xcf'
    TEST_BIP32_PRIVKEY = b'\x045\x83\x94'

    # Public key types:
    PUBLIC_KEY_UNCOMPRESSED = b'\x04'
    PUBLIC_KEY_COMPRESSED_EVEN_Y = b'\x02'
    PUBLIC_KEY_COMPRESSED_ODD_Y = b'\x03'
    PRIVATE_KEY_COMPRESSED_PUBKEY = b'\x01'

    # Units:
    # https://en.bitcoin.it/wiki/Units
    SATOSHI = 1
    uBTC = 10 ** 2
    mBTC = 10 ** 5
    BTC = 10 ** 8

class BitcoinConstants(BaseConstants):
    SUPPORTS_BECH32 = True
    SUPPORTS_SEGWIT = True

class LitecoinConstants(BaseConstants):
    SUPPORTS_BECH32 = True
    SUPPORTS_SEGWIT = True
    # Address formats:
    BECH32_VERSION_SET = ('ltc', 'tltc', 'rltc')  # Versiones Bech32 para Litecoin
    BECH32_MAIN_VERSION_SET = BECH32_VERSION_SET[:1]
    BECH32_TEST_VERSION_SET = BECH32_VERSION_SET[1:]
    MAIN_PUBKEY_HASH = b'\x30'  # Prefijo P2PKH para direcciones mainnet de Litecoin
    MAIN_SCRIPT_HASH = b'\x32'  # Prefijo P2SH para direcciones mainnet de Litecoin
    TEST_PUBKEY_HASH = b'\x6f'  # Prefijo para direcciones P2PKH en Testnet de Litecoin
    TEST_SCRIPT_HASH = b'\x3a'  # Prefijo P2SH para direcciones testnet de Litecoin

    # Keys:
    MAIN_PRIVATE_KEY = b'\xb0'  # Prefijo para claves privadas en Litecoin (WIF)
    MAIN_BIP32_PUBKEY = b'\x04\x88\xb2\x1e'  # Prefijo para claves públicas extendidas en Litecoin (igual a Bitcoin)
    MAIN_BIP32_PRIVKEY = b'\x04\x88\xad\xe4'  # Prefijo para claves privadas extendidas en Litecoin (igual a Bitcoin)
    TEST_PRIVATE_KEY = b'\xef'  # Prefijo para claves privadas en Testnet de Litecoin
    TEST_BIP32_PUBKEY = b'\x04\x35\x87\xcf'  # Prefijo para claves públicas extendidas en Testnet de Litecoin
    TEST_BIP32_PRIVKEY = b'\x04\x35\x83\x94'  # Prefijo para claves privadas extendidas en Testnet de Litecoin

class DogecoinConstants(BaseConstants):
    SUPPORTS_SEGWIT = False  # Dogecoin soporta SegWit, pero no Bech32
    SUPPORTS_BECH32 = False

    # Address formats:
    MAIN_PUBKEY_HASH = b'\x1e'  # Prefijo P2PKH para direcciones mainnet de Dogecoin
    MAIN_SCRIPT_HASH = b'\x16'  # Prefijo P2SH para direcciones mainnet de Dogecoin
    TEST_PUBKEY_HASH = b'\x71'  # Prefijo P2PKH para direcciones testnet de Dogecoin
    TEST_SCRIPT_HASH = b'\xc4'  # Prefijo P2SH para direcciones testnet de Dogecoin

    # Keys:
    MAIN_PRIVATE_KEY = b'\x9e'  # Prefijo para claves privadas en Dogecoin (WIF)
    MAIN_BIP32_PUBKEY = b'\x02\xfa\xca\xfd'  # Prefijo para claves públicas extendidas en Dogecoin
    MAIN_BIP32_PRIVKEY = b'\x02\xfa\xc3\x98'  # Prefijo para claves privadas extendidas en Dogecoin
    TEST_PRIVATE_KEY = b'\xf1'  # Prefijo para claves privadas en Testnet de Dogecoin
    TEST_BIP32_PUBKEY = b'\x04\x32\xa9\xa8'  # Prefijo para claves públicas extendidas en Testnet de Dogecoin
    TEST_BIP32_PRIVKEY = b'\x04\x32\xa9\x42'  # Prefijo para claves privadas extendidas en Testnet de Dogecoin

class DashConstants(BaseConstants):
    SUPPORTS_SEGWIT = False
    SUPPORTS_BECH32 = False

    # Address formats:
    MAIN_PUBKEY_HASH = b'\x4c'  # Prefijo P2PKH para direcciones mainnet de Dash
    MAIN_SCRIPT_HASH = b'\x10'  # Prefijo P2SH para direcciones mainnet de Dash
    TEST_PUBKEY_HASH = b'\x8c'  # Prefijo para direcciones P2PKH en Testnet de Dash
    TEST_SCRIPT_HASH = b'\x13'  # Prefijo P2SH para direcciones testnet de Dash

    # Keys:
    MAIN_PRIVATE_KEY = b'\xcc'  # Prefijo para claves privadas en Dash (WIF)
    MAIN_BIP32_PUBKEY = b'\x02\xfe\x52\xf8'  # Prefijo para claves públicas extendidas en Dash
    MAIN_BIP32_PRIVKEY = b'\x02\xfe\x52\xcc'  # Prefijo para claves privadas extendidas en Dash
    TEST_PRIVATE_KEY = b'\xef'  # Prefijo para claves privadas en Testnet de Dash
    TEST_BIP32_PUBKEY = b'\x03\x1a\x04\x48'  # Prefijo para claves públicas extendidas en Testnet de Dash
    TEST_BIP32_PRIVKEY = b'\x03\x1a\x04\x87'  # Prefijo para claves privadas extendidas en Testnet de Dash

class ZcashConstants(BaseConstants):
    SUPPORTS_SEGWIT = False
    SUPPORTS_BECH32 = False

    # Address formats:
    MAIN_PUBKEY_HASH = b'\x1c\xb8'  # Prefijo P2PKH para direcciones mainnet de Zcash
    MAIN_SCRIPT_HASH = b'\x1c\xbd'  # Prefijo P2SH para direcciones mainnet de Zcash
    TEST_PUBKEY_HASH = b'\x1d\x25'  # Prefijo para direcciones P2PKH en Testnet de Zcash
    TEST_SCRIPT_HASH = b'\x1c\xba'  # Prefijo P2SH para direcciones testnet de Zcash

    # Keys:
    MAIN_PRIVATE_KEY = b'\x80'  # Prefijo para claves privadas en Zcash (WIF)
    MAIN_BIP32_PUBKEY = b'\x02\xaa\x7e\xd3'  # Prefijo para claves públicas extendidas en Zcash
    MAIN_BIP32_PRIVKEY = b'\x02\xaa\x7a\x99'  # Prefijo para claves privadas extendidas en Zcash
    TEST_PRIVATE_KEY = b'\xef'  # Prefijo para claves privadas en Testnet de Zcash
    TEST_BIP32_PUBKEY = b'\x04\x5f\x18\xbc'  # Prefijo para claves públicas extendidas en Testnet de Zcash
    TEST_BIP32_PRIVKEY = b'\x04\x5f\x18\xa8'  # Prefijo para claves privadas extendidas en Testnet de Zcash

class BitcoinCashConstants(BaseConstants):
    SUPPORTS_SEGWIT = False
    SUPPORTS_BECH32 = False  # Bitcoin Cash no usa Bech32, usa CashAddr
    
    # Address formats (CashAddr utiliza un formato diferente, pero conservamos los valores hash160 para la comparación):
    MAIN_PUBKEY_HASH = b'\x00'  # Prefijo P2PKH para direcciones mainnet de Bitcoin Cash
    MAIN_SCRIPT_HASH = b'\x05'  # Prefijo P2SH para direcciones mainnet de Bitcoin Cash
    TEST_PUBKEY_HASH = b'\x6f'  # Prefijo para direcciones P2PKH en Testnet de Bitcoin Cash
    TEST_SCRIPT_HASH = b'\xc4'  # Prefijo P2SH para direcciones testnet de Bitcoin Cash

    # Keys:
    MAIN_PRIVATE_KEY = b'\x80'  # Prefijo para claves privadas en Bitcoin Cash (WIF)
    MAIN_BIP32_PUBKEY = b'\x04\x88\xb2\x1e'  # Prefijo para claves públicas extendidas en Bitcoin Cash (igual que en Bitcoin)
    MAIN_BIP32_PRIVKEY = b'\x04\x88\xad\xe4'  # Prefijo para claves privadas extendidas en Bitcoin Cash (igual que en Bitcoin)
    TEST_PRIVATE_KEY = b'\xef'  # Prefijo para claves privadas en Testnet de Bitcoin Cash
    TEST_BIP32_PUBKEY = b'\x04\x35\x87\xcf'  # Prefijo para claves públicas extendidas en Testnet de Bitcoin Cash
    TEST_BIP32_PRIVKEY = b'\x04\x35\x83\x94'  # Prefijo para claves privadas extendidas en Testnet de Bitcoin Cash

