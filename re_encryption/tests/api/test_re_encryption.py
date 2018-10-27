from users.tests.base import APITestCase
from re_encryption.models import (
    RecordsSet,
    ReEncryption
)


class ReEncryptionPointTestCase(APITestCase):
    def test_creation(self):
        records_set = RecordsSet.objects.create(
            id=1,
            patient=self.get_patient(),
            type='type',
            data='data',
            capsule='capsule'
        )

        data = {
            'records_set_id': 1,
            'recepient_id': self.recepient.id,
            'verifying_key': 'somestr'

        }

        response = self.client.post('/re_encryptions/', data)

        re_encryption = ReEncryption.objects.filter(verifying_key='somestr')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(re_encryption.exists(), True)

        self.client.login(username=self.recepient.email, password='q123sldj23')

        response = self.client.get('/re_encryptions/1/')

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, data)
