from users.tests.base import APITestCase
from re_encryption.models import (
    Delegation,
    RecordsSet
)
from users.models import Recepient


class DelegationPointTestCase(APITestCase):
    def test_creation(self):
        data = {
            'patient_id': 1,
            'recepient_id': 1
        }

        response = self.client.post('/patients/delegations/make/', data)
        recepient = Recepient.objects.get(id=1)
        delegation = Delegation.objects.filter(
            type='add',
            recepient=recepient,
            patient_id=1
        )
        self.assertEqual(delegation.exists(), True)
        self.assertEqual(response.status_code, 201)
