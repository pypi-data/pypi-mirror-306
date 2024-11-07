import re

from mybit.bit_modules.utils import (
    int_to_varint, 
    hex_to_bytes, 
    read_bytes, 
    read_var_string, 
    read_var_int,
    read_segwit_string
)

from mybit.transactions.tx_in_out import (
    TxIn, 
    TxObj, 
    TxOut
)

class TransactionSerializer:
    def __init__(self, constants) -> None:
        self.constants = constants
        
    def serialize(self, tx_obj):
        inp = int_to_varint(len(tx_obj.inputs)) + b''.join(map(bytes, tx_obj.inputs))
        out = int_to_varint(len(tx_obj.outputs)) + b''.join(map(bytes, tx_obj.outputs))
        wit = b''.join([w.witness for w in tx_obj.inputs if w.is_segwit()])
        
        return b''.join([tx_obj.version, self.constants.MARKER if wit else b'', self.constants.FLAG if wit else b'', inp, out, wit, tx_obj.locktime])

    def deserialize(self, tx):
        if isinstance(tx, str) and re.match('^[0-9a-fA-F]*$', tx):
            return self.deserialize(hex_to_bytes(tx))

        segwit_tx = TxObj.is_segwit(self.constants, tx)

        version, tx = read_bytes(tx, 4)

        if segwit_tx:
            _, tx = read_bytes(tx, 1)  # ``marker`` is nulled
            _, tx = read_bytes(tx, 1)  # ``flag`` is nulled

        ins, tx = read_var_int(tx)
        inputs = []

        for i in range(ins):
            txid, tx = read_bytes(tx, 32)
            txindex, tx = read_bytes(tx, 4)
            script_sig, tx = read_var_string(tx)
            sequence, tx = read_bytes(tx, 4)
            inputs.append(TxIn(self.constants, script_sig, txid, txindex, sequence=sequence))

        outs, tx = read_var_int(tx)
        outputs = []

        for _ in range(outs):
            amount, tx = read_bytes(tx, 8)
            script_pubkey, tx = read_var_string(tx)
            outputs.append(TxOut(amount, script_pubkey))

        if segwit_tx:
            for i in range(ins):
                wnum, tx = read_var_int(tx)
                witness = int_to_varint(wnum)

                for _ in range(wnum):
                    w, tx = read_segwit_string(tx)
                    witness += w

                inputs[i].witness = witness

        locktime, _ = read_bytes(tx, 4)

        txobj = TxObj(self.constants, version, inputs, outputs, locktime)

        return txobj