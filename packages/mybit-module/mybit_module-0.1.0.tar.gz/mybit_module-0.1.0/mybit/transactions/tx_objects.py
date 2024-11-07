from mybit.bit_modules.utils import (
    bytes_to_hex,
    hex_to_bytes,
    int_to_varint,
)

class TxIn:
    __slots__ = ('constants', 'script_sig', 'script_sig_len', 'txid', 'txindex', 'witness', 'amount', 'sequence', 'segwit_input')

    def __init__(self, constants, unspent, script_sig, witness=b'', segwit_input=False):
        self.constants = constants
        self.script_sig = script_sig
        self.script_sig_len = int_to_varint(len(script_sig))
        self.txid = hex_to_bytes(unspent.txid)[::-1]
        self.txindex = unspent.txindex.to_bytes(4, byteorder='little')
        self.amount = int(unspent.amount).to_bytes(8, byteorder='little')  # Solo para SegWit
        self.sequence = (unspent.sequence or constants.SEQUENCE).to_bytes(4, byteorder='little')
        self.witness = witness
        self.segwit_input = segwit_input or unspent.segwit

    def __eq__(self, other):
        return (
            self.script_sig == other.script_sig
            and self.script_sig_len == other.script_sig_len
            and self.txid == other.txid
            and self.txindex == other.txindex
            and self.witness == other.witness
            and self.amount == other.amount
            and self.sequence == other.sequence
            and self.segwit_input == other.segwit_input
        )

    def __repr__(self):
        if self.is_segwit():
            return 'TxIn({}, {}, {}, {}, {}, {}, {})'.format(
                repr(self.script_sig),
                repr(self.script_sig_len),
                repr(self.txid),
                repr(self.txindex),
                repr(self.witness),
                repr(self.amount),
                repr(self.sequence),
            )
        return 'TxIn({}, {}, {}, {}, {})'.format(
            repr(self.script_sig), repr(self.script_sig_len), repr(self.txid), repr(self.txindex), repr(self.sequence)
        )

    def __bytes__(self):
        return b''.join([self.txid, self.txindex, self.script_sig_len, self.script_sig, self.sequence])

    def is_segwit(self):
        return self.segwit_input or self.witness


class TxOut:
    __slots__ = ('amount', 'script_pubkey_len', 'script_pubkey')

    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey
        self.script_pubkey_len = int_to_varint(len(script_pubkey))

    def __eq__(self, other):
        return (
            self.amount == other.amount
            and self.script_pubkey == other.script_pubkey
            and self.script_pubkey_len == other.script_pubkey_len
        )

    def __repr__(self):
        return 'TxOut({}, {}, {})'.format(repr(self.amount), repr(self.script_pubkey), repr(self.script_pubkey_len))

    def __bytes__(self):
        return b''.join([self.amount, self.script_pubkey_len, self.script_pubkey])

class TxObj:
    __slots__ = ('constants', 'version', 'TxIn', 'TxOut', 'locktime')

    def __init__(self, constants, version, TxIn, TxOut, locktime):
        self.constants = constants
        segwit_tx = any([i.segwit_input or i.witness for i in TxIn])
        self.version = version
        self.TxIn = TxIn

        if segwit_tx:
            for i in self.TxIn:
                i.witness = i.witness if i.witness else b'\x00'

        self.TxOut = TxOut
        self.locktime = locktime

    def __eq__(self, other):
        return (
            self.version == other.version
            and self.TxIn == other.TxIn
            and self.TxOut == other.TxOut
            and self.locktime == other.locktime
        )

    def __repr__(self):
        return 'TxObj({}, {}, {}, {})'.format(
            repr(self.version), repr(self.TxIn), repr(self.TxOut), repr(self.locktime)
        )

    def __bytes__(self):
        inp = int_to_varint(len(self.TxIn)) + b''.join(map(bytes, self.TxIn))
        out = int_to_varint(len(self.TxOut)) + b''.join(map(bytes, self.TxOut))
        wit = b''.join([w.witness for w in self.TxIn])
        return b''.join([self.version, self.constants.MARKER if wit else b'', self.constants.FLAG if wit else b'', inp, out, wit, self.locktime])

    def legacy_repr(self):
        inp = int_to_varint(len(self.TxIn)) + b''.join(map(bytes, self.TxIn))
        out = int_to_varint(len(self.TxOut)) + b''.join(map(bytes, self.TxOut))
        return b''.join([self.version, inp, out, self.locktime])

    def to_hex(self):
        return bytes_to_hex(bytes(self))

    @classmethod
    def is_segwit(cls, constants, tx):
        if isinstance(tx, cls):
            # Si es un TxObj, lo convertimos a bytes
            tx_bytes = bytes(tx)
        elif isinstance(tx, bytes):
            # Si ya es bytes, no hacemos nada
            tx_bytes = tx
        else:
            # Si es un string hexadecimal, lo convertimos a bytes
            tx_bytes = hex_to_bytes(tx)

        # Comprobamos si los marcadores de SegWit están presentes
        return tx_bytes[4:6] == constants.MARKER + constants.FLAG