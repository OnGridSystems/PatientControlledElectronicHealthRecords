from users.tests.base import APITestCase
from re_encryption.models import RecordsSet
from users.models import Patient
from re_encryption.models import Delegation


class AnonymDataAccessTestCase(APITestCase):
    setup_login_patient = False

    def test_get_patient_own_records(self):
        response = self.client.get('/me/records/')
        self.assertEqual(response.status_code, 403)


class PatientDataAccessTestCase(APITestCase):
    setup_login_patient = True

    def test_patient_own_records(self):
        response = self.client.get('/me/records/')
        print(response.data)


class RecepientDataAccessTestCase(APITestCase):
    setup_login_patient = False
    setup_login_recepient = True

    def test_recepient_delegated_records(self):
        records_set = RecordsSet.objects.create(
            id=1,
            patient=self.get_patient(),
            type='type',
            data='data',
            capsule='capsule'
        )
        Delegation.objects.create(
            recepient=self.recepient,
            type='read',
            records_set=records_set
        )

        response = self.client.get('/records/1/')
        self.assertEqual(response.status_code, 200)


    def test_recepient_not_delegated_records(self):
        records_set = RecordsSet.objects.create(
            id=1,
            patient=self.get_patient(),
            type='type',
            data='data',
            capsule='capsule'
        )

        response = self.client.get('/records/1/')
        self.assertEqual(response.status_code, 403)
