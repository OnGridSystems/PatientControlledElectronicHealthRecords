from users.tests.base import APITestCase
from re_encryption.models import RecordsSet
from users.models import Patient


class AnonymDataAccessTestCase(APITestCase):
    setup_login_patient = False

    def test_get_patient_own_records(self):
        response = self.client.get('/me/records/')
        self.assertEqual(response.status_code, 403)


class PatientDataAccessTestCase(APITestCase):
    def test_patient_own_records(self):
        response = self.client.get('/me/records/')
        print(response.data)
    
    def test_recepient_delegated_records(self):
        records_set = RecordsSet.objects.create(
            patient=self.get_patient(),
            type='type',
            data='data',
            capsule='capsule'
        )
        response = self.client.get('/records/1')
