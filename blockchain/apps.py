from django.apps import AppConfig
from django.conf import settings

from .contracts import PCEHRContract


class BlockchainConfig(AppConfig):
    name = 'blockchain'

    def ready(self):
        self.init_contracts()

    def init_contracts(self):
        PCEHRContract.init(settings.PCEHR_CONTRACT)
