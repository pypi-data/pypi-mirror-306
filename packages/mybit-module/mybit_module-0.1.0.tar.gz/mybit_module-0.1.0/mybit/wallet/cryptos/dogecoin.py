from mybit.utils import read_json

from mybit.wallet.wallet_base import BaseWalletUTXO
from mybit.wallet.cryptos.crypto_constants import DogecoinConstants as constants
from mybit.network.electrum_service import ElectrumService

#agregar network
class Dogecoin(BaseWalletUTXO):
    def __init__(self, wif=None):
        self.constants = constants()
        credentials = read_json('mybit/network/servers.json')['LTC']
        network_api = ElectrumService(host=credentials['host'], port=credentials['port'], proto=credentials['proto'])

        super().__init__(self.constants, wif=wif, version='main', network_api=network_api)

class DogecoinTestnet(BaseWalletUTXO):
    def __init__(self, wif=None):
        self.constants = constants()
        credentials = read_json('mybit/network/servers.json')['LTCTEST']
        network_api = ElectrumService(host=credentials['host'], port=credentials['port'], proto=credentials['proto'])

        super().__init__(self.constants, wif=wif, version='test', network_api=network_api)