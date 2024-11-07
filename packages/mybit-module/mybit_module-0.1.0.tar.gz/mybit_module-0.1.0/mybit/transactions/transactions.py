from itertools import islice

from mybit.wallet.cryptos.crypto_format import CryptoFormat

from mybit.bit_modules.utils import bytes_to_hex, int_to_varint, hex_to_bytes, chunk_data
from mybit.bit_modules.network.rates import currency_to_satoshi_cached
from mybit.bit_modules.crypto import double_sha256, sha256

# from mybit.transactions.transaction_serializer import TransactionSerializer
from mybit.transactions.tx_objects import *

class Transaction:
    def __init__(self, constants):
        self.constants = constants
        self.crypto_format = CryptoFormat(constants)
        self.inputs = []
        self.outputs = []

    def amount_to_satoshis(self, outputs):
        outputs = outputs.copy()

        for i, output in enumerate(outputs):
            dest, amount, currency = output
            outputs[i] = (dest, currency_to_satoshi_cached(amount, currency))

        return outputs

    def construct_outputs(self, outputs):
        outputs_obj = []

        for data in outputs:
            dest, amount = data
            # amount = currency_to_satoshi_cached(amount, currency)

            # P2PKH/P2SH/Bech32
            if amount:
                script_pubkey = self.crypto_format.address_to_scriptpubkey(dest)
                amount = amount.to_bytes(8, byteorder='little')
            # Blockchain storage
            else:
                script_pubkey = self.constants.OP_RETURN + len(dest).to_bytes(1, byteorder='little') + dest
                amount = b'\x00\x00\x00\x00\x00\x00\x00\x00'

            outputs_obj.append(TxOut(amount, script_pubkey))

        return outputs_obj
    
    def construct_inputs(self, unspents):
        inputs = []

        for unspent in unspents:
            script_sig = b''  # empty scriptSig for new unsigned transaction.
            inputs.append(
                TxIn(self.constants, unspent, script_sig)
            )
            
        return inputs
    
    def construct_transaction(self, inputs: list, outputs: list):
        version = self.constants.VERSION_1
        lock_time = self.constants.LOCK_TIME
        return TxObj(self.constants, version, inputs, outputs, lock_time)
    
    def calculate_segwit_preimage(self, tx_obj, input_index, hash_type):
        """Calcula la preimagen para inputs SegWit (BIP-143)"""
        
        # input_count = int_to_varint(len(tx_obj.TxIn))
        output_block = b''.join([bytes(o) for o in tx_obj.TxOut])

        # Hashes requeridos por BIP-143
        hashPrevouts = double_sha256(b''.join([i.txid + i.txindex for i in tx_obj.TxIn]))
        hashSequence = double_sha256(b''.join([i.sequence for i in tx_obj.TxIn]))
        hashOutputs = double_sha256(output_block)

        # Cálculo de la preimagen para el input SegWit
        preimage = sha256(
            tx_obj.version
            + hashPrevouts
            + hashSequence
            + tx_obj.TxIn[input_index].txid
            + tx_obj.TxIn[input_index].txindex
            + tx_obj.TxIn[input_index].script_sig_len
            + tx_obj.TxIn[input_index].script_sig  # scriptCode length
            + tx_obj.TxIn[input_index].sequence  # scriptCode (incluye cantidad)
            + hashOutputs
            + tx_obj.locktime
            + hash_type
        )

        return preimage

    def calculate_non_segwit_preimage(self, tx_obj, input_index, hash_type):
        """Calcula la preimagen para inputs no SegWit"""
        
        input_count = int_to_varint(len(tx_obj.TxIn))
        output_count = int_to_varint(len(tx_obj.TxOut))
        output_block = b''.join([bytes(o) for o in tx_obj.TxOut])

        # Cálculo de la preimagen para el input no SegWit
        preimage = sha256(
            tx_obj.version
            + input_count
            + b''.join(
                ti.txid + ti.txindex + self.constants.OP_0 + ti.sequence
                for ti in islice(tx_obj.TxIn, input_index)
            )
            + tx_obj.TxIn[input_index].txid
            + tx_obj.TxIn[input_index].txindex
            + tx_obj.TxIn[input_index].script_sig_len
            + tx_obj.TxIn[input_index].script_sig  # scriptCode length
            + tx_obj.TxIn[input_index].sequence  # scriptCode
            + b''.join(
                ti.txid + ti.txindex + self.constants.OP_0 + ti.sequence
                for ti in islice(tx_obj.TxIn, input_index + 1, None)
            )
            + output_count
            + output_block
            + tx_obj.locktime
            + hash_type
        )

        return preimage

    def calculate_preimages(self, tx_obj, inputs_parameters):
        """Calcula las preimágenes para cada input en la transacción, diferenciando entre SegWit y no SegWit."""
        
        preimages = []
        
        for input_index, hash_type, segwit_input in inputs_parameters:
            # Validar que hash_type sea soportado
            if hash_type != self.constants.HASH_TYPE:
                raise ValueError('Solo se soporta hashType de valor 1.')

            # Llamar a la función correcta dependiendo de si el input es SegWit o no
            if segwit_input:
                preimage = self.calculate_segwit_preimage(tx_obj, input_index, hash_type)
            else:
                preimage = self.calculate_non_segwit_preimage(tx_obj, input_index, hash_type)

            preimages.append(preimage)
        
        return preimages
    
    def build_preimages_inputs(self, private_key, sign_inputs, tx, input_dict):
        # Make input parameters for preimage calculation
        inputs_parameters = []

        # The TxObj in `tx` will below be modified to contain the scriptCodes used
        # for the transaction structure to be signed

        # `input_script_field` copies the scriptSigs for partially signed
        # transactions to later extract signatures from it:
        input_script_field = [tx.TxIn[i].script_sig for i in range(len(tx.TxIn))]

        for i in sign_inputs:
            # Create transaction object for preimage calculation
            tx_input = tx.TxIn[i].txid + tx.TxIn[i].txindex
            segwit_input = input_dict[tx_input]['segwit']
            tx.TxIn[i].segwit_input = segwit_input

            script_code = private_key.scriptcode
            script_code_len = int_to_varint(len(script_code))

            # Use scriptCode for preimage calculation of transaction object:
            tx.TxIn[i].script_sig = script_code
            tx.TxIn[i].script_sig_len = script_code_len

            if segwit_input:
                try:
                    tx.TxIn[i].script_sig += input_dict[tx_input]['amount'].to_bytes(8, byteorder='little')

                    # For partially signed Segwit transactions the signatures must
                    # be extracted from the witnessScript field:
                    input_script_field[i] = tx.TxIn[i].witness
                except AttributeError:
                    raise ValueError(
                        'Cannot sign a segwit input when the input\'s amount is '
                        'unknown. Maybe no network connection or the input is '
                        'already spent? Then please provide all inputs to sign as '
                        '`Unspent` objects to the function call.'
                    )

            inputs_parameters.append([i, self.constants.HASH_TYPE, segwit_input])

        return inputs_parameters
    
    # def calc_txid(self, tx_hex):
    #     tx_obj = self.deserialize(self.constants, tx_hex)
    #     return bytes_to_hex(double_sha256(tx_obj.legacy_repr())[::-1])

    def to_bytes(self):
        inp = int_to_varint(len(self.inputs)) + b''.join(map(bytes, self.inputs))
        out = int_to_varint(len(self.outputs)) + b''.join(map(bytes, self.outputs))
        wit = b''.join([w.witness for w in self.inputs if w.is_segwit()])
        return b''.join([self.constants.VERSION_1, self.constants.MARKER if wit else b'', self.constants.FLAG if wit else b'', inp, out, wit, self.constants.LOCK_TIME])

    def to_hex(self):
        return bytes_to_hex(self.to_bytes())

    # @classmethod
    # def deserialize(self, constants, tx_bytes):
    #     tx_obj = TransactionSerializer.deserialize(constants, tx_bytes)
    #     return tx_obj