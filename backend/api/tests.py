from django.contrib.auth import authenticate
from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from api.models import *
import random
from datetime import date
import json
class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.language = LANGUAGE.objects.create(name='English', ISO_639_1='en', ISO_639_2='eng')
        self.language = LANGUAGE.objects.create(name='Polish', ISO_639_1='pl', ISO_639_2='pol')
        self.user1 = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com',
                                              lang='en')
        self.user2 = User.objects.create_user(username='testuser1', password='testpassword', email='test1@example.com',
                                              lang='en')
        self.genre = GENRE.objects.create(name='RTS', description='Real time strategy')

    def test_login(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(reverse('login'), data, content_type="application/json")
        data = response.json()
        self.assertEqual(data['status'], 'Login successful')

    def test_register(self):
        data = {
            'email': 'tesaat{}@example.com'.format(random.getrandbits(5)),
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

    def test_set_description1(self):
        self.client.logout()
        data = {'description' : 'test'}
        response = self.client.post(reverse('user_set_description'), data, content_type="application/json")
        data_response = response.json()
        self.assertFalse(data_response['status'])
        self.assertEqual(data_response['mess'], 'Authorisation fail.')

    def test_set_description2(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('user_set_description')+ "?description=test")
        data_response = response.json()
        self.assertFalse(data_response['status'])
        self.assertEqual(data_response['mess'], 'Authorisation fail.')

    def test_set_description3(self):
        self.client.login(username='testuser', password='testpassword')
        data = {'description' : 'test'}
        response = self.client.post(reverse('user_set_description'), data, content_type="application/json")
        data_response = response.json()
        self.assertTrue(data_response['status'])
        self.assertEqual(data_response['mess'], 'User description updated.')
        self.assertEqual(data_response['description'], 'test')
        self.assertEqual(User.objects.get(username='testuser').description, 'test')


    def test_change_password1(self):
        self.client.logout()
        data = {'password': 'testpassword', 'new_password1' : 'testpassword2', 'new_password2': 'testpassword2'}
        response = self.client.post(reverse('change_password'), data, content_type="application/json")
        data_response = response.json()
        self.assertFalse(data_response['status'])
        self.assertEqual(data_response['mess'], 'Authorisation fail.')

    def test_change_password2(self):
        User.objects.create_user(username='testuser_change_password', password='testpassword', email='test123@example.com',
                                 lang='en')
        user = User.objects.get(username='testuser_change_password')
        self.client.login(username='testuser_change_password', password='testpassword')
        data = {'password': 'testpassword', 'new_password1' : 'testpassword2', 'new_password2': 'testpassword2'}
        response = self.client.post(reverse('change_password'), data, content_type="application/json")
        data_response = response.json()
        self.assertTrue(data_response['status'])
        self.assertEqual(data_response['mess'], 'User password updated.')
        self.assertFalse(self.client.login(username='testuser_change_password', password='testpassword'))
        self.assertTrue(self.client.login(username='testuser_change_password', password='testpassword2'))

        user.delete()

    def test_change_password3(self):
        User.objects.create_user(username='testuser_change_password', password='testpassword', email='test123@example.com',
                                 lang='en')
        user = User.objects.get(username='testuser_change_password')
        self.client.login(username='testuser_change_password', password='testpassword')
        data = {'password': '', 'new_password1' : 'testpassword2', 'new_password2': 'testpassword2'}
        response = self.client.post(reverse('change_password'), data, content_type="application/json")
        data_response = response.json()
        self.assertFalse(data_response['status'])
        self.assertEqual(data_response['mess'], 'Not a valid password.')

        user.delete()

    def test_change_password4(self):
        User.objects.create_user(username='testuser_change_password', password='testpassword', email='test123@example.com',
                                 lang='en')
        user = User.objects.get(username='testuser_change_password')
        self.client.login(username='testuser_change_password', password='testpassword')
        data = {'password': 'testpassword', 'new_password1' : 'testpassword', 'new_password2': 'testpassword2'}
        response = self.client.post(reverse('change_password'), data, content_type="application/json")
        data_response = response.json()
        self.assertFalse(data_response['status'])
        self.assertEqual(data_response['mess'], 'Fail passwords are not the same.')
        user.delete()

class FriendshipViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.language = LANGUAGE.objects.create(name='English', ISO_639_1='en', ISO_639_2='eng')

        self.user1 = User.objects.create_user(username='user1', password='password1', email='test111111@example.com',
                                              lang='en')
        self.user2 = User.objects.create_user(username='user2', password='password2', email='test222222@example.com',
                                              lang='en')
        self.friendship = FRIENDSHIP.objects.create(user1=self.user1, user2=self.user2, create_date=date.today())

    def test_add_friendship(self):
        url = reverse('add_friendship')
        self.client.force_login(self.user1)
        data = {'pk': self.user2.pk}
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], True)
        self.assertEqual(response.json()['mess'], 'Invition sent.')

    def test_add_friendship_self_invite(self):
        url = reverse('add_friendship')
        self.client.force_login(self.user1)
        data = {'pk': self.user1.pk}
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], False)
        self.assertEqual(response.json()['mess'], 'You can\'t invite to friend yourself.')

    def test_add_friendship_invalid_user(self):
        url = reverse('add_friendship')
        self.client.force_login(self.user1)
        data = {'pk': 999}
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], False)
        self.assertEqual(response.json()['mess'], 'User don\'t found.')

    def test_active_friendship_invite(self):
        url = reverse('active_friendship_invite')
        self.client.force_login(self.user2)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], True)
        self.assertEqual(response.json()['list'][str(self.friendship.pk)], self.user1.username)

    def test_accept_invite(self):
        url = reverse('accept_invite')
        self.client.force_login(self.user2)
        data = {'pk': self.friendship.pk}
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], True)
        self.assertEqual(response.json()['mess'], 'Invition accepted.')

    def test_accept_invite_invalid_user(self):
        url = reverse('accept_invite')
        self.client.force_login(self.user1)
        data = {'pk': self.friendship.pk}
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], False)
        self.assertEqual(response.json()['mess'], 'Authorisation fail.')

    def test_accept_invite_invalid_invite(self):
        url = reverse('accept_invite')
        self.client.force_login(self.user2)
        data = {'pk': 999}
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], False)
        self.assertEqual(response.json()['mess'], 'Invition dosn\'t exist.')

    def test_accept_invite_unauthenticated_user(self):
        url = reverse('accept_invite')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], False)
        self.assertEqual(response.json()['mess'], 'Authorisation fail.')

class ProfileViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.language = LANGUAGE.objects.create(ISO_639_1='en', ISO_639_2='eng', name='English')
        self.language1 = LANGUAGE.objects.create(ISO_639_1='pl', ISO_639_2='pol', name='Polish')
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.local', lang=self.language)
        self.user.lang.add(self.language)

    def test_get_my_profile(self):
        url = reverse('get_my_profile')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], True)
        self.assertEqual(response.json()['username'], self.user.username)
        self.assertEqual(response.json()['email'], self.user.email)
        self.assertEqual(
            response.json()['lang'],
            {
                self.language.name: {
                    'ISO_639_1': self.language.ISO_639_1,
                    'ISO_639_2': self.language.ISO_639_2
                }
            }
        )

    def test_get_my_profile_unauthenticated(self):
        url = reverse('get_my_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], False)
        self.assertEqual(response.json()['mess'], 'Authorisation fail.')

#Additional test gen by chatGBT
class ViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.language = LANGUAGE.objects.create(ISO_639_1='en', ISO_639_2='eng', name='English')
        self.user = User.objects.create_user(username='testuser', password='testpassword', lang=self.language, email="example@example.com")
        self.friend = User.objects.create_user(username='friend', password='friendpassword', lang=self.language, email="example2@example.com")
        self.friendship = FRIENDSHIP.objects.create(user1=self.user, user2=self.friend, create_date=date.today())

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Mess'], 'This is the api.')

    def test_login_valid_credentials(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(reverse('login'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'Login successful')

    def test_login_invalid_credentials(self):
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(reverse('login'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'Login failed')

    def test_log_out(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'Logout success.')

    def test_register(self):
        data = {
            'email': 'test@example.com',
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
            'language': 'en'
        }
        response = self.client.post(reverse('register'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'Create new user success')

    def test_is_auth_session_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('is_auth_session'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['LoginStatus'])
        self.assertEqual(response.json()['username'], 'testuser')

    def test_is_auth_session_not_authenticated(self):
        response = self.client.get(reverse('is_auth_session'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['LoginStatus'])

    def test_get_csrf_token(self):
        response = self.client.get(reverse('get_csrf_token'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('csrf_token' in response.json())

    def test_get_lang_list(self):
        response = self.client.get(reverse('get_lang_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(list(response.json().keys())[0], 'English')

    def test_get_lang(self):
        response = self.client.get(reverse('get_lang'), {'name': 'English'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(list(response.json().keys())[0], 'English')

    def test_user_set_description_authenticated(self):
        self.client.force_login(self.user)
        data = {'description': 'Test description'}
        response = self.client.post(reverse('user_set_description'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['status'])
        self.assertEqual(response.json()['mess'], 'User description updated.')
        self.assertEqual(response.json()['description'], 'Test description')

    def test_user_set_description_not_authenticated(self):
        data = {'description': 'Test description'}
        response = self.client.post(reverse('user_set_description'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['status'])
        self.assertEqual(response.json()['mess'], 'Authorisation fail.')

    def test_change_password_authenticated_valid_passwords(self):
        self.client.force_login(self.user)
        data = {'password': 'testpassword', 'new_password1': 'newpassword', 'new_password2': 'newpassword'}
        response = self.client.post(reverse('change_password'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['status'])
        self.assertEqual(response.json()['mess'], 'User password updated.')

    def test_change_password_authenticated_invalid_passwords(self):
        self.client.force_login(self.user)
        data = {'password': 'testpassword', 'new_password1': 'newpassword', 'new_password2': 'wrongpassword'}
        response = self.client.post(reverse('change_password'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['status'])
        self.assertEqual(response.json()['mess'], 'Fail passwords are not the same.')

    def test_change_password_not_authenticated(self):
        data = {'password': 'testpassword', 'new_password1': 'newpassword', 'new_password2': 'newpassword'}
        response = self.client.post(reverse('change_password'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['status'])
        self.assertEqual(response.json()['mess'], 'Authorisation fail.')

    def test_add_friendship_authenticated_user_exists(self):
        self.client.force_login(self.user)
        data = {'pk': self.friend.pk}
        response = self.client.post(reverse('add_friendship'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['status'])
        self.assertEqual(response.json()['mess'], 'Invition sent.')

    def test_add_friendship_authenticated_user_does_not_exist(self):
        self.client.force_login(self.user)
        data = {'pk': 999}
        response = self.client.post(reverse('add_friendship'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['status'])
        self.assertEqual(response.json()['mess'], 'User don\'t found.')

    def test_add_friendship_not_authenticated(self):
        data = {'pk': self.friend.pk}
        response = self.client.post(reverse('add_friendship'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['status'])
        self.assertEqual(response.json()['mess'], 'Authorisation fail.')

    def test_active_friendship_invite_authenticated(self):
        self.client.force_login(self.friend)
        response = self.client.post(reverse('active_friendship_invite'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['status'])
        self.assertTrue('list' in response.json())

    def test_active_friendship_invite_not_authenticated(self):
        response = self.client.post(reverse('active_friendship_invite'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['status'])
        self.assertEqual(response.json()['mess'], 'Authorisation fail.')

    def test_accept_invite_authenticated_invitation_exists(self):
        self.client.force_login(self.friend)
        invitation = FRIENDSHIP.objects.create(user1=self.user, user2=self.friend, create_date=date.today(), active=False)
        data = {'pk': invitation.pk}
        response = self.client.post(reverse('accept_invite'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['status'])
        self.assertEqual(response.json()['mess'], 'Invition accepted.')

    def test_accept_invite_authenticated_invitation_does_not_exist(self):
        self.client.force_login(self.friend)
        data = {'pk': 999}
        response = self.client.post(reverse('accept_invite'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['status'])
        self.assertEqual(response.json()['mess'], 'Invition dosn\'t exist.')

    def test_accept_invite_not_authenticated(self):
        data = {'pk': 1}
        response = self.client.post(reverse('accept_invite'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['status'])
        self.assertEqual(response.json()['mess'], 'Authorisation fail.')

    def test_get_my_profile_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('get_my_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['status'])
        self.assertEqual(response.json()['username'], self.user.username)
        self.assertEqual(response.json()['email'], self.user.email)
        self.assertTrue('lang' in response.json())

    def test_get_my_profile_not_authenticated(self):
        response = self.client.get(reverse('get_my_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['status'])
        self.assertEqual(response.json()['mess'], 'Authorisation fail.')

# Finsh chatGBT tests
class TestSearchUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.language = LANGUAGE.objects.create(ISO_639_1='en', ISO_639_2='eng', name='English')
        self.user = User.objects.create_user(username='testuser', password='testpassword', lang=self.language, email="example@example.com")
        self.user1 = User.objects.create_user(username='testuser1', password='testpassword', lang=self.language, email="example1@example.com")
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword', lang=self.language, email="example2@example.com")
        self.user3 = User.objects.create_user(username='testuser3', password='testpassword', lang=self.language, email="example3@example.com")
        self.user4 = User.objects.create_user(username='testuser4', password='testpassword', lang=self.language, email="example4@example.com")
        self.user5 = User.objects.create_user(username='testuser5', password='testpassword', lang=self.language, email="example5@example.com")
        self.user6 = User.objects.create_user(username='user', password='testpassword', lang=self.language, email="exampl6@example.com")
        self.user7 = User.objects.create_user(username='user1', password='testpassword', lang=self.language, email="example7@example.com")
        self.user8 = User.objects.create_user(username='user2', password='testpassword', lang=self.language, email="example8@example.com")
        self.user9 = User.objects.create_user(username='user3', password='testpassword', lang=self.language, email="example9@example.com")
    def test_list_of_all_user_post(self):
        response = self.client.post(reverse('get_users'), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertEqual(len(response_data['list']), 10)
        self.assertTrue(response_data['status'])
        self.assertEqual(response_data['mess'], 'Operation success.')

    def test_list_of_all_user_invalid_post_contest_type(self):
        response = self.client.post(reverse('get_users'), content_type='test')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertFalse(response_data['status'])
        self.assertEqual(response_data['mess'], 'Wrong content type.')

    def test_list_of_all_user(self):
        response = self.client.get(reverse('get_users'))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertEqual(len(response_data['list']), 10)
        self.assertTrue(response_data['status'])
        self.assertEqual(response_data['mess'], 'Operation success.')

    def test_list_of_username_chose_like_user(self):
        data = {'username': 'user%'}
        response = self.client.post(reverse('get_users'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertTrue(response_data['status'])
        self.assertEqual(response_data['mess'], 'Operation success.')
        self.assertEqual(len(response_data['list']), 4)

    def test_list_of_username_chose_like_all_character(self):
        data = {'username': '%'}
        response = self.client.post(reverse('get_users'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertTrue(response_data['status'])
        self.assertEqual(response_data['mess'], 'Operation success.')
        self.assertEqual(len(response_data['list']), 10)

    def test_list_of_email_chose_like_user(self):
        data = {'email': '%1%'}
        response = self.client.post(reverse('get_users'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertTrue(response_data['status'])
        self.assertEqual(response_data['mess'], 'Operation success.')
        self.assertEqual(len(response_data['list']), 1)

    def test_list_of_email_chose_like_all_character(self):
        data = {'email': '%'}
        response = self.client.post(reverse('get_users'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertTrue(response_data['status'])
        self.assertEqual(response_data['mess'], 'Operation success.')
        self.assertEqual(len(response_data['list']), 10)