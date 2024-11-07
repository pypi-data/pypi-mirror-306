from mybit.bit_modules.crypto import ripemd160_sha256
from mybit.bit_modules.utils import hex_to_bytes, bytes_to_hex, int_to_varint, script_push

from mybit.wallet.base_key import BaseKey
from mybit.transactions.transactions import Transaction
from mybit.transactions.utxo_selector import UTXOSelector
from mybit.transactions.tx_objects import TxObj
from mybit.transactions.unspent import Unspent

from mybit.transactions.script_hash_converter import ScriptHashConverter

class BaseWalletUTXO(BaseKey):
    def __init__(self, constants, wif=None, version='main', network_api=None):
        super().__init__(constants, wif=wif)

        self.version = version
        self.network_api = network_api
        self.transaction = Transaction(constants)
        self.scripthash = ScriptHashConverter(constants)

        self._address = None
        self._segwit_address = None
        self._segwit_address_native = None
        self._scriptcode = None
        self._segwit_scriptcode = None

        self.balance = 0
        self.unspents = []
        self.transactions = []

    @property
    def address(self):
        """The public address you share with others to receive funds."""
        if self._address is None:
            self._address = self.crypto_format.public_key_to_address(self._public_key, version=self.version)
        return self._address

    @property
    def segwit_address(self):
        """The public segwit nested in P2SH address you share with others to
        receive funds."""
        # Only make segwit address if public key is compressed
        if self._segwit_address is None and self.is_compressed():
            self._segwit_address = self.crypto_format.public_key_to_segwit_address(self._public_key, version=self.version)
        return self._segwit_address
    
    @property
    def segwit_address_native(self):
        """
        The public segwit nested in p2wpkh address you share with others to receive funds.
        """
        # Only make segwit address if public key is compressed
        if self._segwit_address_native is None and self.is_compressed():
            self._segwit_address_native = self.crypto_format.public_key_to_p2wpkh_address(self._public_key, version=self.version)
        return self._segwit_address_native

    @property
    def scriptcode(self):
        self._scriptcode = self.crypto_format.address_to_scriptpubkey(self.address)
        return self._scriptcode

    @property
    def segwit_scriptcode(self):
        self._segwit_scriptcode = self.constants.OP_0 + self.constants.OP_PUSH_20 + ripemd160_sha256(self.public_key)
        return self._segwit_scriptcode
    
    def can_sign_unspent(self, unspent):
        script = bytes_to_hex(self.crypto_format.address_to_scriptpubkey(self.address))
        script_segwit = bytes_to_hex(self.crypto_format.address_to_scriptpubkey(self.segwit_address))
        script_segwit_native = bytes_to_hex(self.crypto_format.address_to_scriptpubkey(self.segwit_address_native))

        return (unspent.script == script or unspent.script == script_segwit or unspent.script == script_segwit_native)
    
    def get_can_sign_unspents(self, selected_utxos):
        input_dict = {}
        
        try:
            for unspent in selected_utxos:
                if not self.can_sign_unspent(unspent):
                    continue
                tx_input = hex_to_bytes(unspent.txid)[::-1] + unspent.txindex.to_bytes(4, byteorder='little')
                input_dict[tx_input] = unspent.to_dict()
        except TypeError:
            raise TypeError(
                'Please provide as unspents at least all inputs to be signed with the function call in a list.'
            )
        
        return input_dict
        
    def get_utxos(self, address):
        script_hash = self.scripthash.get_scripthash(address)
        script_pubkey = bytes_to_hex(self.crypto_format.address_to_scriptpubkey(address))
        get_utxos = self.network_api.get_filtered_utxos(script_hash)

        if not len(get_utxos) > 0:
            return []
        
        utxos = []
        utxos.extend(
            Unspent(
                utxo['value'],
                utxo['confirmations'],
                script_pubkey,
                utxo['tx_hash'],
                utxo['tx_pos'],
            )
            for utxo in get_utxos
        )

        return utxos

    def get_unspents(self):
        """
        Fetches all available unspent transaction outputs.
        """
        #TODO agregar soporte para transacciones segwit para criptomonedas que no soportan BECH32

        if self.address:
            utxos = self.get_utxos(self.address)

            self.unspents += list(
                map(
                    lambda u: u.set_type('p2pkh' if self.is_compressed() else 'p2pkh-uncompressed'), utxos
                )
            )

        # Se obtienen los utxos de las direcciones en formato segwit si la crypto lo soporta
        if self.constants.SUPPORTS_BECH32:
            if self.segwit_address:
                utxos = self.get_utxos(self.segwit_address)
                self.unspents += list(map(lambda u: u.set_type('np2wkh'), utxos))

            if self.segwit_address_native:
                utxos = self.get_utxos(self.segwit_address_native)
                self.unspents += list(map(lambda u: u.set_type('p2wpkh'), utxos))

            self.balance = sum(unspent.amount for unspent in self.unspents)

        return self.unspents
    
    def create_transaction(
        self,
        outputs: list,
        fee=None,
        absolute_fee=False,
        leftover=None,
        combine=True,
        message=None,
        unspents=None,
        message_is_hex=False,
        replace_by_fee=False,
    ):  # pragma: no cover

        unspents = self.get_unspents()

        if not unspents:
            raise ValueError('Transactions must have at least one unspent.')
        
        outputs = self.transaction.amount_to_satoshis(outputs)

        utxo_selector = UTXOSelector(fee)
        target_amount = sum(out[1] for out in outputs)
        total_outputs = len(outputs)
        selected_utxos, total_fee, total_change = utxo_selector.branch_and_bound(unspents, target_amount, total_outputs)

        for output in outputs:
            addres, _ = output
            address_version = self.crypto_format.get_version(addres)

            if address_version and address_version != self.version:
                raise ValueError('Cannot send to ' + self.version + 'net address when spending from a ' + address_version  + 'net address.')

        if total_change != None and total_change > 0:
            change_address = leftover if leftover != None else self.segwit_address_native
            outputs.append((change_address, total_change))

        
        tx_in = self.transaction.construct_inputs(selected_utxos)
        tx_out = self.transaction.construct_outputs(outputs)
        unsigned_tx = self.transaction.construct_transaction(tx_in, tx_out)

        return unsigned_tx, selected_utxos
    
    def sign_transaction(self, private_key, tx, *, unspents):
        can_unspents = self.get_can_sign_unspents(unspents)

        sign_inputs = [j for j, i in enumerate(tx.TxIn) if i.txid + i.txindex in can_unspents]

        segwit_tx = TxObj.is_segwit(self.constants, tx)
        public_key = self.public_key
        public_key_push = script_push(len(public_key))

        # Make input parameters for preimage calculation
        inputs_parameters = self.transaction.build_preimages_inputs(self, sign_inputs, tx, can_unspents)
        preimages = self.transaction.calculate_preimages(tx, inputs_parameters)

        # Calculate signature scripts:
        for hash, (i, _, segwit_input) in zip(preimages, inputs_parameters):
            signature = private_key.sign(hash) + b'\x01'

            if segwit_input:
                script_sig = b''  # For SegWit inputs, scriptSig must be empty
                witness = (
                    b'\x02'  # witness items count
                    + len(signature).to_bytes(1, byteorder='little')  # signature length
                    + signature
                    + public_key_push
                    + public_key
                )
            else:
                # For non-SegWit inputs, scriptSig contains the signature and public key
                script_sig = (
                    len(signature).to_bytes(1, byteorder='little')  # Push signature length
                    + signature
                    + public_key_push
                    + public_key
                )
                witness = b''  # No witness for non-SegWit

            # Providing the signature(s) to the input
            tx.TxIn[i].script_sig = script_sig
            tx.TxIn[i].script_sig_len = int_to_varint(len(script_sig))
            tx.TxIn[i].witness = witness

        return tx.to_hex()
    

    def send_transaction(        
        self,
        outputs: list,
        fee=None,
        absolute_fee=False,
        leftover=None,
        combine=True,
        message=None,
        unspents=None,
        message_is_hex=False,
        replace_by_fee=False,
    ):
        create_transaction = self.create_transaction(outputs, fee)
        unsigned_tx, selected_utxos = create_transaction

        tx_signed = self.sign_transaction(self, unsigned_tx, unspents=selected_utxos)
        
        return self.network_api.send_transaction(tx_signed), tx_signed
    
    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.address}>'