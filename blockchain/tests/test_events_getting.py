from .base import BlockChainTestCase
from blockchain.contracts import PCEHRContract


class EventsGettingTestCase(BlockChainTestCase):
    setup_eth_tester = True
    setup_contracts = ['PCEHR']
    health_records_sets_types = ['allergies', 'infections']

    @classmethod
    def _setup_PCEHR(cls):
        PCEHR = cls.web3.eth.contract(abi=PCEHRContract.get_compiled()['abi'],
                                      bytecode=PCEHRContract.get_compiled()['bin'])
        health_records_sets_types = [r_type.encode('utf-8') for r_type in cls.health_records_sets_types]
        tx_hash = PCEHR.constructor(health_records_sets_types).transact()
        tx_receipt = cls.web3.eth.getTransactionReceipt(tx_hash)
        cls.pcehr_contract = cls.web3.eth.contract(address=tx_receipt.contractAddress,
                                                   abi=PCEHRContract.get_compiled()['abi'])

        PCEHRContract.init({'address': cls.pcehr_contract.address})

    def register_patient(self, from_acc, proxy_id, pub_key):
        return self.pcehr_contract.functions.registerPatient(proxy_id, pub_key).transact({
            'gas': 100000,
            'from': from_acc
        }).hex()

    def test_kek(self):
        patient_address = self.account['address']
