from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from django.conf import settings
from web3.gas_strategies.rpc import rpc_gas_price_strategy


class Web3NotAvailableException(Exception):
    def __init__(self, rpc_url):
        self.rpc_url = rpc_url

    def __str__(self):
        return f'WEB3_RPC_URL: {self.rpc_url}'


_web3_instance = None


def get_web3():
    global _web3_instance

    if not _web3_instance:
        _web3_instance = Web3(HTTPProvider(settings.WEB3_RPC_URL, request_kwargs={'timeout': 300}))
        _web3_instance.eth.setGasPriceStrategy(rpc_gas_price_strategy)
        if getattr(settings, 'RINKEBY_MIDDLEWARE', True):
            _web3_instance.middleware_stack.inject(geth_poa_middleware, layer=0)

    if not _web3_instance.isConnected():
        _web3_instance = None

        raise Web3NotAvailableException(settings.WEB3_RPC_URL)

    return _web3_instance
