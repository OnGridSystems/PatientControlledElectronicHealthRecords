from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from proxy.utils.datetime import datetime
from users.models import Patient
from blockchain.tests.base import BlockChainTestCase


class APITestCase(TestCase):
    first_name = 'Gordon'
    last_name = 'Freeman'
    email = 'gordon@example.com'
    password = 'q123sldj23'
    eth_account = '0x73015966604928A312F79F7E69291a656Cb88602'
    priv_key = '067ab0aedbc8ebe6a8a6404bd2f29a4d152a6db052bd2d396f188e26f1c37c27'
    pub_key = '02d425658bdc98cd02c041a2e720a27ef380764b2a6ce59d7c10403bcdee355b76'

    setup_login = True

    def setUp(self):
        self.user = User.objects.create(
            username=self.email,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name
        )
        self.user.set_password(self.password)
        self.user.save()

        patient = Patient.objects.create(
            user=self.user,
            eth_address=self.eth_account,
            pub_key=self.pub_key
        )
        patient.save()

        self._patient_id = patient.id      

        self.client = APIClient()

        if self.setup_login:
            self.client.login(username=self.email, password=self.password)

    def get_patient(self):
        return Patient.objects.get(id=self._patient_id)

    def tearDown(self):
        datetime.stubed_now = None
        datetime.stubed_utcnow = None

    def stub_datetime_now(self, dt):
        datetime.stubed_now = dt

    def stub_datetime_utcnow(self, dt):
        datetime.stubed_utcnow = dt
