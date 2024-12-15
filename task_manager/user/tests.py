from django.test import TestCase
from task_manager.user.models import User
from task_manager.user.forms import UserForm
from django.urls import reverse
from django.contrib.messages import get_messages


class TestAuthentication(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_login(self):
        login_successful = self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        self.assertTrue(login_successful, "User login failed")
        login_unsuccessful = self.client.login(
            username=self.user.username,
            password="wrong_password"
        )
        self.assertFalse(
            login_unsuccessful, "User login should have failed but it passed"
        )

    def test_logout(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        self.client.logout()
        response = self.client.get(reverse('user_update', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('login'))


class TestUserCreate(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.complete_user_data = {
            "username": "complete_user",
            "password1": "correct_password",
            "password2": "correct_password",
            "first_name": "John",
            "last_name": "Smith"
        }
        self.missing_field_user_data = {
            "username": "missing_field_user",
            "password1": "correct_password",
            "password2": "correct_password",
            "first_name": "John"
        }
        self.user = User.objects.get(id=1)
        self.duplicate_user_data = {
            "username": "testuser",
            "password1": "test",
            "password2": "test",
            "first_name": "Jane",
            "last_name": "Doe"
        }

    def test_create_user_success(self):
        response = self.client.post(
            reverse('user_create'), self.complete_user_data
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='complete_user')
        self.assertIsNotNone(user)
        self.assertTrue(User.objects.filter(username="complete_user").exists())

    def test_create_user_missing_field(self):
        response = self.client.post(
            reverse('user_create'), self.missing_field_user_data
        )
        form = response.context['form']
        self.assertFormError(form, 'last_name', 'This field is required.')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="missing_field_user").exists()
        )

    def test_create_duplicate_username(self):
        response = self.client.post(
            reverse('user_create'), self.duplicate_user_data
        )
        form = response.context['form']
        self.assertFormError(
            form, 'username', 'A user with this username already exists.'
        )
        self.assertEqual(response.status_code, 200)


class TestUserRead(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_read_users_unauthorized(self):
        response = self.client.get(reverse('user_index'))
        self.assertEqual(response.status_code, 200)

    def test_read_users_authorized(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.get(reverse('user_index'))
        self.assertEqual(response.status_code, 200)

    def test_read_nonexistent(self):
        response = self.client.get('/wrong_url/')
        self.assertEqual(response.status_code, 404)


class TestUserUpdate(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user = User.objects.get(id=2)

    def test_update_user_success(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(
            reverse('user_update', kwargs={'pk': 2}),
            {
                'username': 'new_username',
                'password1': 'correct_password',
                'password2': 'correct_password',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'new_username')

    def test_update_user_missing_field(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(
            reverse('user_update', kwargs={'pk': 2}),
            {
                'username': 'new_username',
                'password1': 'correct_password',
                'password2': 'correct_password',
                'last_name': 'Doe'
            }
        )
        form = response.context['form']
        self.assertFormError(form, 'first_name', 'This field is required.')
        self.assertEqual(response.status_code, 200)

    def test_update_other_user(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.get(reverse('user_update', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('user_index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(
            str(messages[0]),
            "You don't have permission to edit this user."
        )

    def test_update_user_unauthorized(self):
        response = self.client.get(reverse('user_update', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(
            str(messages[0]),
            "You are not logged in! Please log in."
        )


class TestUserDelete(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_delete_user_success(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(reverse('user_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_index'))
        self.assertFalse(User.objects.filter(id=1).exists())

    def test_delete_other_user(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(reverse('user_delete', kwargs={'pk': 2}))
        self.assertRedirects(response, reverse('user_index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(
            str(messages[0]),
            "You don't have permission to edit this user."
        )
        self.assertTrue(User.objects.filter(id=2).exists())

    def test_delete_user_unauthorized(self):
        response = self.client.post(reverse('user_delete', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(
            str(messages[0]),
            "You are not logged in! Please log in."
        )
