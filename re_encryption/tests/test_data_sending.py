from umbral import (
    signing, config,
    pre, keys
)
from umbral.fragments import KFrag
from umbral.params import UmbralParameters
from umbral.curve import SECP256K1

from users.tests.base import APITestCase
from re_encryption.models import RecordsSet
from users.models import Patient
from re_encryption.models import (
    Delegation,
    KeyFragment
)


class RecepientDataSendingCase(APITestCase):
    setup_login_patient = False

    def test_recepient_add_records_set(self):
        config.set_default_curve(SECP256K1)

        patient_private_key = keys.UmbralPrivateKey.gen_key()
        patient_public_key = patient_private_key.get_pubkey()
        recepient_private_key = keys.UmbralPrivateKey.gen_key()
        recepient_public_key = recepient_private_key.get_pubkey()

        recepient_signing_key = keys.UmbralPrivateKey.gen_key()
        recepient_verifying_key = recepient_signing_key.get_pubkey()
        recepient_signer = signing.Signer(private_key=recepient_signing_key)

        hexed_patient_public_key = patient_public_key.to_bytes().hex()
        hexed_recepient_public_key = recepient_public_key.to_bytes().hex()

        data = {
            'first_name': 'Gordo',
            'last_name': 'Freema',
            'email': 'patient@example.com',
            'password': 'q123sldj23',
            'eth_address': '0x73015966604928A312F79F7E69291a656Cb88603',
            'pub_key': hexed_patient_public_key
        }

        response = self.client.post('/patients/signup/', data)

        data = {
            'organisation_id': 'someseriousorganisationidentifier',
            'first_name': 'Gordon',
            'last_name': 'Freeman',
            'email': 'recepient@example.com',
            'password': 'q123sldj23',
            'eth_address': '0x73015966604928A312F79F7E69291a656Cb88603',
            'pub_key': hexed_recepient_public_key
        }

        response = self.client.post('/recepients/signup/', data)

        self.client.login(username='patient@example.com', password='q123sldj23')

        data = {
            'patient_id': 2,
            'recepient_id': 2
        }

        response = self.client.post('/patients/delegations/make/', data)

        self.client.login(username='recepient@example.com', password='q123sldj23')

        plaintext = b'Proxy Re-encryption is cool!'
        ciphertext, capsule = pre.encrypt(recepient_public_key, plaintext)
        kfrags = pre.generate_kfrags(delegating_privkey=recepient_private_key,
                                     signer=recepient_signer,
                                     receiving_pubkey=patient_public_key,
                                     threshold=10,
                                     N=20)

        data = {
            'patient_id': 2,
            'type': 'type',
            'data': ciphertext.hex(),
            'capsule': capsule.to_bytes().hex()
        }
        response = self.client.post('/records/add/', data)

        for kfrag in kfrags:
            data = {
                'delegation_id': 1,
                'bytes': kfrag.to_bytes().hex()
            }
            self.client.post('/patients/kfrags/', data)
        
        self.client.login(username='patient@example.com', password='q123sldj23')

        response = self.client.get('/me/records/')

        from_proxy_capsule = bytes.fromhex(response.data[0]['capsule'])
        from_proxy_data = bytes.fromhex(response.data[0]['data'])

        umbral_parameteres = UmbralParameters(SECP256K1)
        
        from_proxy_capsule = pre.Capsule.from_bytes(
            from_proxy_capsule,
            umbral_parameteres
        )

        from_proxy_capsule.set_correctness_keys(
            delegating=recepient_public_key,
            receiving=patient_public_key,
            verifying=recepient_verifying_key
        )

        response = self.client.get('/patients/kfrags/')

        from_proxy_kfrags = [KFrag.from_bytes(bytes.fromhex(kfrag['bytes'])) for kfrag in response.data]

        for kfrag in from_proxy_kfrags:
            cfrag = pre.reencrypt(kfrag, from_proxy_capsule)
            from_proxy_capsule.attach_cfrag(cfrag)

        cleartext = pre.decrypt(
            ciphertext=from_proxy_data,
            capsule=from_proxy_capsule,
            decrypting_key=patient_private_key
        )

        self.assertEqual(cleartext, plaintext)
