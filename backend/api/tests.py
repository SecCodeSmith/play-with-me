from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from api.models import LANGUAGE, USER as User
import random


class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.language = LANGUAGE.objects.create(name='English', ISO_639_1='en', ISO_639_2='eng')
        self.language = LANGUAGE.objects.create(name='Polish', ISO_639_1='pl', ISO_639_2='pol')
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com',
                                             lang='en')

    def test_login(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(reverse('login'), data, content_type="application/json")
        data = response.json()
        self.assertEqual(data['status'], 'Login successful')

    def test_register(self):
        data = {
            'email': 'test{}@example.com'.format(random.getrandbits(5)),
            'username': 'newuser{}'.format(random.getrandbits(5)),
            'password1': 'password',
            'password2': 'password',
            'language': 'en'}
        response = self.client.post(reverse('register'), data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data_res = response.json()
        self.assertEqual(data_res['status'], 'Create new user success', msg=data_res)
        data = {'username': data['username'], 'password': data['password1']}
        response = self.client.post(reverse('login'), data, content_type="application/json")
        data = response.json()
        self.assertEqual(data['status'], 'Login successful')

    def test_get_csrf_token(self):
        response = self.client.get(reverse('get_csrf_token'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue('csrf_token' in data)

    def test_is_auth_session_authenticated1(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('is_auth_session'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['LoginStatus'])
        self.assertEqual(data['username'], 'testuser')

    def test_is_auth_session_authenticated2(self):
        self.client.logout()
        response = self.client.get(reverse('is_auth_session'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['LoginStatus'])

    def test_is_auth_session_not_authenticated(self):
        response = self.client.get(reverse('is_auth_session'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['LoginStatus'])

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'Logout success.')
        response = self.client.get(reverse('is_auth_session'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['LoginStatus'])

    def test_get_lang_list(self):
        response = self.client.get(reverse('get_lang_list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)  # Assuming you have only created one language in the setup
        self.assertEqual(data['English']['ISO_639_1'], 'en')
        self.assertEqual(data['English']['ISO_639_2'], 'eng')

    def test_get_lang1(self):
        response = self.client.get(reverse('get_lang') + '?ISO_639_1=en')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1, data)  # Assuming you have only created one language in the setup
        self.assertEqual(data['English']['ISO_639_1'], 'en')
        self.assertEqual(data['English']['ISO_639_2'], 'eng')

    def test_get_lang2(self):
        response = self.client.get(reverse('get_lang') + '?ISO_639_2=eng')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1, data)  # Assuming you have only created one language in the setup
        self.assertEqual(data['English']['ISO_639_1'], 'en')
        self.assertEqual(data['English']['ISO_639_2'], 'eng')

    def test_get_lang3(self):
        response = self.client.post(reverse('get_lang'), {'ISO_639_1': 'en'}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1, data)  # Assuming you have only created one language in the setup
        self.assertEqual(data['English']['ISO_639_1'], 'en')
        self.assertEqual(data['English']['ISO_639_2'], 'eng')

    def test_get_lang4(self):
        response = self.client.post(reverse('get_lang'), {'ISO_639_2': 'eng'}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1, data)  # Assuming you have only created one language in the setup
        self.assertEqual(data['English']['ISO_639_1'], 'en')
        self.assertEqual(data['English']['ISO_639_2'], 'eng')

    def test_index1(self):
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['Mess'], 'This is the api.')
    def test_index2(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['Mess'], 'This is the api.')
        self.assertTrue(data['LoginStatus'])
        