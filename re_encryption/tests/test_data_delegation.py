from users.tests.base import APITestCase
from re_encryption.models import (
    Delegation,
    RecordsSet
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
        print(response.data)
        #self.assertEqual(response.status_code, 201)
