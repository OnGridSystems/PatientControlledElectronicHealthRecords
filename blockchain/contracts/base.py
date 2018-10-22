import json
from django.conf import settings
from blockchain.web3 import get_web3
from proxy.utils.logger import LoggerMixin


class BaseContract(LoggerMixin):
    @classmethod
    def get_compiled(cls):
        if not hasattr(cls, '_compiled'):
            with open(cls.compiled_file_path.format(BASE_DIR=settings.BASE_DIR)) as f:
                cls._compiled = json.load(f)

        return cls._compiled

    @classmethod
    def init(cls, settings):
        cls._settings = settings
        cls.contract_address = settings['address']

    @property
    def web3(self):
        return get_web3()

    @property
    def contract(self):
        return self.web3.eth.contract(abi=self.get_compiled()['abi'],
                                      address=self.contract_address)
