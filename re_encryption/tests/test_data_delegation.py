from users.tests.base import APITestCase
from re_encryption.models import (
    Delegation,
    RecordsSet,
    KeyFragment
)


class PatientDataAccessTestCase(APITestCase):
    def test_patient_make_records_delegation(self):
        records_set = RecordsSet.objects.create(
            id=1,
            patient=self.get_patient(),
            type='type',
            data='data',
            capsule='capsule'
        )

        data = {
            'type': 'write',
            'records_set_id': 1,
            'recepient_id': 1,
            'key_fragments': ['key', 'fragments']
        }

        response = self.client.post('/records/delegations/make/', data)
        self.assertEqual(response.status_code, 201)

    def test_patient_make_add_delegation(self):
        data = {
            'patient_id': 1,
            'recepient_id': 1
        }

        response = self.client.post('/patients/delegations/make/', data)
        self.assertEqual(response.status_code, 201)
    
    def test_key_fragments_sending(self):
        Delegation.objects.create(
            recepient=self.recepient,
            patient_id=self.get_patient().id,
            type='add'
        )
        data = {
            'delegation_id': 1,
            'bytes': 'kek'
        }

        response = self.client.post('/patients/kfrags/', data)
        self.assertEqual(response.status_code, 201)

        kfrag = KeyFragment.objects.filter(bytes='kek')
        self.assertEqual(kfrag.exists(), True)
