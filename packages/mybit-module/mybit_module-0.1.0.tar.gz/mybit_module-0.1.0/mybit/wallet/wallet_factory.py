from typing import Union, Tuple
from mybit.wallet.cryptos import *

class WalletFactory:
    wallet_types = {
        'BTC': Bitcoin,
        'BTCTEST': BitcoinTestnet,
        'LTC': Litecoin,
        'LTCTEST': LitecoinTestnet,
        'DOGE': Dogecoin,
        'DOGETEST': DogecoinTestnet,
    }

    @staticmethod
    def get_supported_cryptos() -> Tuple[str, ...]:
        return tuple(WalletFactory.wallet_types.keys())

    @staticmethod
    def get_wallet(coin: str, wif: str = None) -> Union['Bitcoin', 'BitcoinTestnet', 'Litecoin', 'LitecoinTestnet', 'Dogecoin', 'DogecoinTestnet']:
        wallet_class = WalletFactory.wallet_types.get(coin)
        if wallet_class:
            return wallet_class(wif=wif)
        else:
            raise ValueError("Unsupported cryptocurrency type")
        
    @staticmethod
    def get_wallet_info(coin: str) -> Union['Bitcoin.Info', 'BitcoinTestnet.Info', 'Litecoin.Info', 'LitecoinTestnet.Info', 'Dogecoin.Info', 'DogecoinTestnet.Info']:
        wallet_class = WalletFactory.wallet_types.get(coin)
        if wallet_class:
            return wallet_class().Info()
        else:
            raise ValueError("Unsupported cryptocurrency type")