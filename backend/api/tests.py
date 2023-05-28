from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from api.models import LANGUAGE
import random

User = get_user_model()

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.language = LANGUAGE.objects.create(name='English', ISO_639_1='en', ISO_639_2='eng')

    def test_login(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(reverse('login'), json=data, content_type="application/json")
        data = response.json()
        self.assertEqual(data['status'], 'Login successful')

    def test_register(self):
        response = self.client.post(reverse('register'), {
            'email': 'test{}@example.com'.format(random.getrandbits(5)),
            'username': 'newuser{}'.format(random.getrandbits(5)),
            'password1': 'password',
            'password2': 'password',
            'language': self.language.name}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'Create new user success', msg=data)

    def test_get_csrf_token(self):
        response = self.client.get(reverse('get_csrf_token'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue('csrf_token' in data)

    def test_is_auth_session_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('is_auth_session'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['LoginStatus'])
        self.assertEqual(data['username'], 'testuser')

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
        self.assertEqual(len(data), 1)  # Assuming you have only created one language in the setup
        self.assertEqual(data['English']['ISO_639_1'], 'en')
        self.assertEqual(data['English']['ISO_639_2'], 'eng')
