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
        #Generate keys
        config.set_default_curve(SECP256K1)

        patient_private_key = keys.UmbralPrivateKey.gen_key()
        patient_public_key = patient_private_key.get_pubkey()
        recepient_private_key = keys.UmbralPrivateKey.gen_key()
        recepient_public_key = recepient_private_key.get_pubkey()

        recepient_signing_key = keys.UmbralPrivateKey.gen_key()
        recepient_verifying_key = recepient_signing_key.get_pubkey()
        recepient_signer = signing.Signer(private_key=recepient_signing_key)

        #Convert keys to hex
        hexed_patient_public_key = patient_public_key.to_bytes().hex()
        hexed_recepient_public_key = recepient_public_key.to_bytes().hex()
        hexed_recepient_verifying_key = recepient_verifying_key.to_bytes().hex()

        #Signup patient
        data = {
            'first_name': 'Gordo',
            'last_name': 'Freema',
            'email': 'patient@example.com',
            'password': 'q123sldj23',
            'eth_address': '0x73015966604928A312F79F7E69291a656Cb88603',
            'pub_key': hexed_patient_public_key
        }

        response = self.client.post('/patients/signup/', data)

        #Signup recepient
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

        #Log in as patient
        self.client.login(username='patient@example.com', password='q123sldj23')

        data = {
            'patient_id': 2,
            'recepient_id': 2
        }

        #Delegate add records permission to recepient
        response = self.client.post('/patients/delegations/make/', data)

        #Log in as recepient
        self.client.login(username='recepient@example.com', password='q123sldj23')

        #Encrypt message
        plaintext = b'Proxy Re-encryption is cool!'
        ciphertext, capsule = pre.encrypt(recepient_public_key, plaintext)
        kfrags = pre.generate_kfrags(delegating_privkey=recepient_private_key,
                                     signer=recepient_signer,
                                     receiving_pubkey=patient_public_key,
                                     threshold=10,
                                     N=20)
        #Add encrypted record
        data = {
            'patient_id': 2,
            'type': 'type',
            'data': ciphertext.hex(),
            'capsule': capsule.to_bytes().hex()
        }

        response = self.client.post('/records/add/', data)

        self.assertEqual(response.status_code, 201)

        #Add kfrags 
        for kfrag in kfrags:
            data = {
                'delegation_id': 1,
                'bytes': kfrag.to_bytes().hex()
            }
            self.client.post('/patients/kfrags/', data)
        
        #Add verifying_key
        data = {
            'records_set_id': 1,
            'recepient_id': 3,
            'verifying_key': hexed_recepient_verifying_key
        }

        response = self.client.post('/re_encryptions/', data)
        
        #Login as patient
        self.client.login(username='patient@example.com', password='q123sldj23')

        response = self.client.get('/me/records/')

        from_proxy_capsule = bytes.fromhex(response.data[0]['capsule'])
        from_proxy_data = bytes.fromhex(response.data[0]['data'])

        umbral_parameteres = UmbralParameters(SECP256K1)

        from_proxy_capsule = pre.Capsule.from_bytes(
            from_proxy_capsule,
            umbral_parameteres
        )

        response = self.client.get('/patients/kfrags/')
        """
        Patient can receive kfrags for each re_encryption
        """

        from_proxy_kfrags = [KFrag.from_bytes(bytes.fromhex(kfrag['bytes'])) for kfrag in response.data]

        response = self.client.get('/re_encryptions/1/')
        from_proxy_verifying_key = bytes.fromhex(response.data['verifying_key'])

        """
        Patient gets verifying_key
        """

        from_proxy_verifying_key = keys.UmbralPublicKey.from_bytes(
            from_proxy_verifying_key,
            params=umbral_parameteres
        )

        from_proxy_capsule.set_correctness_keys(
            delegating=recepient_public_key,
            receiving=patient_public_key,
            verifying=from_proxy_verifying_key
        )


        for kfrag in from_proxy_kfrags:
            cfrag = pre.reencrypt(kfrag, from_proxy_capsule)
            from_proxy_capsule.attach_cfrag(cfrag)

        cleartext = pre.decrypt(
            ciphertext=from_proxy_data,
            capsule=from_proxy_capsule,
            decrypting_key=patient_private_key
        )

        """
        Patient opens the capsule to decrypt records
        organisation added. Then patient can reencrypt whole
        records to delegate editing and reading permissions
        to other organisations
        """

        self.assertEqual(cleartext, plaintext)
