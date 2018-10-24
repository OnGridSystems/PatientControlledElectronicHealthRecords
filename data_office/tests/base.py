from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from proxy.utils.datetime import datetime
from data_office.models import Patient
from blockchain.tests.base import BlockChainTestCase


class PatientAPITestCase(TestCase):
    first_name = 'Gordon'
    last_name = 'Freeman'
    email = 'gordon@example.com'
    password = 'q123sldj23'
    eth_account = '0x73015966604928A312F79F7E69291a656Cb88602'
    priv_key = b"\x06z\xb0\xae\xdb\xc8\xeb\xe6\xa8\xa6@K\xd2\xf2\x9aM\x15*m\xb0R\xbd-9o\x18\x8e&\xf1\xc3|'"
    pub_key = b'\x02\xd4%e\x8b\xdc\x98\xcd\x02\xc0A\xa2\xe7 \xa2~\xf3\x80vK*l\xe5\x9d|\x10@;\xcd\xee5[v'

    setup_login = True

    def setUp(self):
        user = User.objects.create(
            username=self.email,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name
        )
        user.set_password(self.password)
        user.save()

        patient = Patient.objects.create(
            user=user,
            eth_address=self.eth_account,
            pub_key=self.pub_key
        )  

        self._patient_id = patient.id      

        self.client = APIClient()

        if self.setup_login:
            self.client.login(email=self.email, password=self.password)

    def get_patient(self):
        return Patient.objects.get(id=self._patient_id)

    def tearDown(self):
        datetime.stubed_now = None
        datetime.stubed_utcnow = None

    def stub_datetime_now(self, dt):
        datetime.stubed_now = dt

    def stub_datetime_utcnow(self, dt):
        datetime.stubed_utcnow = dt
