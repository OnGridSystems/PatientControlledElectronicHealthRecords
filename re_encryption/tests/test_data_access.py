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
        self.assertEqual(response.status_code, 200)


class RecepientDataAccessTestCase(APITestCase):
    setup_login_patient = False
    setup_login_recepient = True

    def test_get_delegated_records(self):
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

    def test_get_not_delegated_records(self):
        records_set = RecordsSet.objects.create(
            id=1,
            patient=self.get_patient(),
            type='type',
            data='data',
            capsule='capsule'
        )

        response = self.client.get('/records/1/')
        self.assertEqual(response.status_code, 403)
    
    def test_add_delegated_records(self):
        Delegation.objects.create(
            recepient=self.recepient,
            patient_id=self.get_patient().id,
            type='add'
        )
        
        data = {
            'patient_id': self.get_patient().id,
            'type': 'type',
            'data': 'data',
            'capsule': 'capsule'
        }
        response = self.client.post('/records/add/', data)
        self.assertEqual(response.status_code, 201)

        self.client.login(username=self.get_patient().email, password='q123sldj23')
        response = self.client.get('/me/records/')
        self.assertEqual(response.status_code, 200)

    def test_add_not_delegated_records(self):
        data = {
            'patient_id': self.get_patient().id,
            'type': 'type',
            'data': 'data',
            'capsule': 'capsule'
        }
        response = self.client.post('/records/add/', data)
        self.assertEqual(response.status_code, 403)

    def test_update_delegated_records(self):
        records_set = RecordsSet.objects.create(
            id=1,
            patient=self.get_patient(),
            type='type',
            data='data',
            capsule='capsule'
        )

        Delegation.objects.create(
            recepient=self.recepient,
            type='write',
            records_set=records_set
        )

        data = {
            'data': 'data22',
            'capsule': 'capsule2'
        }
        response = self.client.put('/records/edit/1/', data)
        self.assertEqual(response.status_code, 200)

    def test_update_not_delegated_records(self):
        records_set = RecordsSet.objects.create(
            id=1,
            patient=self.get_patient(),
            type='type',
            data='data',
            capsule='capsule'
        )

        data = {
            'data': 'data22',
            'capsule': 'capsule2'
        }
        response = self.client.put('/records/edit/1/', data)
        self.assertEqual(response.status_code, 403)
