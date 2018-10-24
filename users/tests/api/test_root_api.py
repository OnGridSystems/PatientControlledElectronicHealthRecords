from ..base import APITestCase


class RootTestCase(APITestCase):
    def test_kek(self):
        response = self.client.get('/patients/1/')
        print(response.data)
