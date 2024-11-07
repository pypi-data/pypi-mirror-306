from mybit.utils import read_json_servers

from mybit.wallet.wallet_base import BaseWalletUTXO
from mybit.wallet.cryptos.crypto_info import CryptoInfo
from mybit.wallet.cryptos.crypto_constants import LitecoinConstants as constants
from mybit.network.electrum_service import ElectrumService

def initialize_constants_and_network(version='main'):
    """Método estático para inicializar constants, credentials y network_api"""
    constants_instance = constants()
    network_key = 'LTC' if version == 'main' else 'LTCTEST'
    credentials = read_json_servers()[network_key]
    network_api = ElectrumService(host=credentials['host'], port=credentials['port'], proto=credentials['proto'])
    return constants_instance, network_api

class Litecoin(BaseWalletUTXO):
    @staticmethod
    def get_version():
        return 'main'

    class Info:
        """Clase interna para manejar las consultas de información de transacciones y direcciones"""
        def __init__(self):
            version = Litecoin.get_version()
            # Usamos el método de inicialización centralizado
            self.constants, self.network_api = initialize_constants_and_network(version)
            # Instancia CryptoInfo
            self.crypto_info = CryptoInfo(self.constants, version=version, network_api=self.network_api)

        def get_utxos(self, address: str, confirmations: int = 1):
            """Obtiene los UTXOs de una dirección"""
            return self.crypto_info.get_utxos(address, confirmations)

        def get_balance(self, address: str) -> int:
            """Obtiene el balance de una dirección"""
            return self.crypto_info.get_balance(address)

        def check_transaction_status(self, txid: str) -> dict:
            """Verifica el estado de una transacción"""
            return self.crypto_info.check_transaction_status(txid)

        def get_transaction_details(self, txid: str) -> dict:
            """Obtiene los detalles completos de una transacción"""
            return self.crypto_info.get_transaction_details(txid)

        def is_valid_address(self, address: str) -> bool:
            """Verifica si una dirección es válida"""
            return self.crypto_info.is_valid_address(address)

    def __init__(self, wif=None):
        version = Litecoin.get_version()
        # Usamos el método centralizado
        self.constants, self.network_api = initialize_constants_and_network(version)
        super().__init__(self.constants, wif=wif, version=version, network_api=self.network_api)

class LitecoinTestnet(BaseWalletUTXO):
    @staticmethod
    def get_version():
        return 'test'
    
    class Info:
        """Clase interna para manejar las consultas de información de transacciones y direcciones"""
        def __init__(self):
            version = LitecoinTestnet.get_version()
            # Usamos el método de inicialización centralizado
            self.constants, self.network_api = initialize_constants_and_network(version)
            # Instancia CryptoInfo
            self.crypto_info = CryptoInfo(self.constants, version=version, network_api=self.network_api)

        # Declaración explícita de métodos para que el editor los reconozca
        def get_utxos(self, address: str, confirmations: int = 1):
            return self.crypto_info.get_utxos(address, confirmations)

        def get_balance(self, address: str) -> int:
            return self.crypto_info.get_balance(address)

        def check_transaction_status(self, txid: str) -> dict:
            return self.crypto_info.check_transaction_status(txid)

        def get_transaction_details(self, txid: str) -> dict:
            return self.crypto_info.get_transaction_details(txid)

        def is_valid_address(self, address: str) -> bool:
            return self.crypto_info.is_valid_address(address)

    def __init__(self, wif=None):
        version = LitecoinTestnet.get_version()
        # Usamos el método centralizado
        self.constants, self.network_api = initialize_constants_and_network(version)
        super().__init__(self.constants, wif=wif, version=version, network_api=self.network_api)