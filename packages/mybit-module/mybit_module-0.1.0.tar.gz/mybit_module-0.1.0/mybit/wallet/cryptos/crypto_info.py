from mybit.transactions.script_hash_converter import ScriptHashConverter
from mybit.wallet.cryptos.crypto_format import CryptoFormat

class CryptoInfo:
    def __init__(self, constants, version='main', network_api=None):
        self.version = version
        self.network_api = network_api
        self.scripthash = ScriptHashConverter(constants)
        self.cryptoformat = CryptoFormat(constants)

    def get_address_scripthash(self, address):
        return self.scripthash.get_scripthash(address)
    
    def get_utxos(self, address, min_confirmations=1):
        script_hash = self.scripthash.get_scripthash(address)
        get_utxos = self.network_api.get_filtered_utxos(script_hash, min_confirmations)

        if not len(get_utxos) > 0:
            return []
        
        return get_utxos
    
    def get_balance(self, address):
        script_hash = self.scripthash.get_scripthash(address)
        get_balance = self.network_api.get_address_balance(script_hash)
        
        return int(get_balance['result']['confirmed']) or 0

    def check_transaction_status(self, txid: str, min_confirmations=3):
        """
        Verifica el estado de una transacción dada su txid y devuelve el número de confirmaciones y el estado de la transacción.

        :param txid: El ID de la transacción a verificar.
        :returns: Un diccionario con el número de confirmaciones y el estado de la transacción.
        """
        # Obtener los detalles de la transacción desde la red (o de un servicio externo)
        transaction_details = self.network_api.get_transaction_details(txid)

        if 'error' in transaction_details:
            return {
                'status': 'failed',
                'confirmations': 0
            }

        # Obtener el número de confirmaciones de la transacción
        confirmations = transaction_details['result'].get('confirmations', 0)

        # Definir el estado de la transacción basado en el número de confirmaciones
        if confirmations == 0:
            status = 'pending'
        elif confirmations > 0 and confirmations >= min_confirmations:
            status = 'confirmed'
        else:
            status = 'unknown'

        # Devolver un diccionario con el estado y las confirmaciones
        return {
            'status': status,
            'confirmations': confirmations
        }

    def get_transaction_details(self, txid: str):
        """Obtiene los detalles completos de una transacción"""
        get_transaction = self.network_api.get_transaction_details(txid)

        return get_transaction['result'] if not 'error' in get_transaction else None

    def is_valid_address(self, address):
        return self.cryptoformat.validate_address(address, self.version)