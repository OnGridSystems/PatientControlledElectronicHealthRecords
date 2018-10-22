from django.test import TestCase
from web3 import Web3, HTTPProvider, EthereumTesterProvider
from eth_tester import EthereumTester
from django.conf import settings
from django.apps import apps

import blockchain.web3
from proxy.utils.datetime import datetime
from blockchain.contracts import PCEHRContract
from blockchain.apps import BlockchainConfig


class BlockChainTestCase(TestCase):
    setup_eth_tester = False
    setup_contracts = []  # PCEHR

    def stub_datetime_now(self, dt):
        datetime.stubed_now = dt

    def stub_datetime_utcnow(self, dt):
        datetime.stubed_utcnow = dt

    @classmethod
    def _setup_account(cls):
        cls.account = settings.ETH_ACCOUNT

        cls.eth_tester.add_account(cls.account['private_key'])

        cls.eth_tester.send_transaction({
            'from': cls.eth_tester.get_accounts()[0],
            'to': cls.account['address'],
            'gas': 21000,
            'value': 100 * 10 ** 18,
        })

    @classmethod
    def _setup_contracts(cls):
        cls.web3.eth.defaultAccount = cls.account['address']

        for c in cls.setup_contracts:
            getattr(cls, f'_setup_{c}')()

    @classmethod
    def take_snapshot(cls):
        return cls.eth_tester.take_snapshot()

    @classmethod
    def patch_web3(cls):
        blockchain.web3._web3_instance = cls.web3

    @classmethod
    def setUpTestData(cls):
        if cls.setup_eth_tester:
            cls.eth_tester = EthereumTester()
            cls.web3 = Web3(EthereumTesterProvider(cls.eth_tester))
            cls.patch_web3()

            cls._setup_account()
            cls._setup_contracts()

            cls.base_snapshot_id = cls.take_snapshot()
        else:
            cls.web3 = Web3(HTTPProvider(settings.WEB3_RPC_URL))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        if cls.setup_eth_tester:
            apps.get_app_config('blockchain').init_contracts()

    def setUp(self):
        if self.setup_eth_tester:
            self.eth_tester.enable_auto_mine_transactions()
            self.eth_tester.revert_to_snapshot(self.base_snapshot_id)

        self.utcnow = datetime.utcnow()
        self.stub_datetime_utcnow(self.utcnow)
