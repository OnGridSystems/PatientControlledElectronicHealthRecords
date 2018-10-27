from django.urls import reverse

from ..base import APITestCase


class SignupTestCase(APITestCase):
    setup_login_patient = False

    def test_signup(self):
        data = {
            'first_name': 'Gordo',
            'last_name': 'Freema',
            'email': 'gordn@example.com',
            'password': 'q123sldj23',
            'eth_address': '0x73015966604928A312F79F7E69291a656Cb88603',
            'pub_key': '02d425658bdc98cd02c041a2e720a27ef380764b2a6ce59d7c10403bcdee355b76'
        }
        response = self.client.post('/patients/signup/', data)

        return_data = {
            'first_name': 'Gordo',
            'last_name': 'Freema',
            'eth_address': '0x73015966604928A312F79F7E69291a656Cb88603',
            'pub_key': '02d425658bdc98cd02c041a2e720a27ef380764b2a6ce59d7c10403bcdee355b76',
            'user_id': 3
        }

        self.assertDictEqual(response.data, return_data)
