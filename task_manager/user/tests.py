import json
from os.path import join

from django.urls import reverse
from django.utils.translation import gettext as _

from task_manager.user.models import User
from task_manager.utils import BaseTestCase

FIXTURE_PATH = 'task_manager/fixtures/'


class TestAuthentication(BaseTestCase):

    def setUp(self):
        self.user = User.objects.all().first()

    def test_login(self):
        login_successful = self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        self.assertTrue(login_successful, _("User login failed"))
        login_unsuccessful = self.client.login(
            username=self.user.username,
            password="wrong_password"
        )
        self.assertFalse(
            login_unsuccessful, _("User login should have failed but it passed")
        )

    def test_logout(self):
        self.login_user(self.user)
        self.client.logout()
        response = self.client.get(reverse('user_update', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('login'))


class TestUserCreate(BaseTestCase):

    def setUp(self):
        self.user = User.objects.all().first()
        with open(join(FIXTURE_PATH, "users_test_data.json")) as f:
            self.users_data = json.load(f)
        self.complete_user_data = self.users_data.get("create_complete")
        self.missing_field_user_data = self.users_data.get(
            "create_missing_field"
        )
        self.duplicate_user_data = self.users_data.get("create_duplicate")

    def test_create_user_success(self):
        response = self.client.post(
            reverse('user_create'), self.complete_user_data, follow=True
        )
        user = User.objects.get(username='complete_user')
        self.assertIsNotNone(user)
        self.assertTrue(User.objects.filter(username="complete_user").exists())
        self.assertRedirectWithMessage(
            response, 'login', _("User is registered successfully")
        )

    def test_create_user_missing_field(self):
        response = self.client.post(
            reverse('user_create'), self.missing_field_user_data
        )
        form = response.context['form']
        self.assertFormError(form, 'last_name', _('This field is required.'))
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
            form, 'username', _('A user with that username already exists.')
        )
        self.assertEqual(response.status_code, 200)


class TestUserRead(BaseTestCase):

    def setUp(self):
        self.user = User.objects.all().first()

    def test_read_users_unauthorized(self):
        response = self.client.get(reverse('user_index'))
        self.assertEqual(response.status_code, 200)

    def test_read_users_authorized(self):
        self.login_user(self.user)
        response = self.client.get(reverse('user_index'))
        self.assertEqual(response.status_code, 200)

    def test_read_nonexistent(self):
        response = self.client.get('/wrong_url/')
        self.assertEqual(response.status_code, 404)


class TestUserUpdate(BaseTestCase):

    def setUp(self):
        self.user = User.objects.get(id=2)
        with open(join(FIXTURE_PATH, "users_test_data.json")) as f:
            self.users_data = json.load(f)
        self.complete_user_data = self.users_data.get("update_complete")
        self.missing_field_user_data = self.users_data.get(
            "update_missing_field"
        )
        self.duplicate_user_data = self.users_data.get("update_duplicate")

    def test_update_user_success(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('user_update', kwargs={'pk': 2}),
            self.complete_user_data, follow=True
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'new_username')
        self.assertRedirectWithMessage(
            response, 'user_index', _("User is updated successfully")
        )

    def test_update_user_missing_field(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('user_update', kwargs={'pk': 2}),
            self.missing_field_user_data
        )
        form = response.context['form']
        self.assertFormError(form, 'first_name', _('This field is required.'))
        self.assertEqual(response.status_code, 200)

    def test_update_duplicate_username(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('user_update', kwargs={'pk': 2}),
            self.duplicate_user_data
        )
        form = response.context['form']
        self.assertFormError(
            form, 'username', _('A user with that username already exists.')
        )
        self.assertEqual(response.status_code, 200)

    def test_update_other_user(self):
        self.login_user(self.user)
        response = self.client.get(
            reverse('user_update', kwargs={'pk': 1}), follow=True
        )
        self.assertRedirectWithMessage(
            response, 'user_index',
            _("You don't have permission to edit this user.")
        )

    def test_update_user_unauthorized(self):
        response = self.client.get(
            reverse('user_update', kwargs={'pk': 1}), follow=True
        )
        self.assertRedirectWithMessage(response)


class TestUserDelete(BaseTestCase):

    def setUp(self):
        self.user = User.objects.get(id=3)
        self.user_in_use = User.objects.get(id=1)

    def test_delete_user_success(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('user_delete', kwargs={'pk': 3}), follow=True
        )
        self.assertFalse(User.objects.filter(id=3).exists())
        self.assertRedirectWithMessage(
            response, 'user_index', _("User is deleted successfully")
        )

    def test_delete_user_in_use(self):
        self.login_user(self.user_in_use)
        response = self.client.post(
            reverse('user_delete', kwargs={'pk': 1}), follow=True
        )
        self.assertTrue(User.objects.filter(id=3).exists())
        self.assertRedirectWithMessage(
            response, 'user_index',
            _("Cannot delete user while they are in use")
        )

    def test_delete_other_user(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('user_delete', kwargs={'pk': 2}), follow=True
        )
        self.assertTrue(User.objects.filter(id=2).exists())
        self.assertRedirectWithMessage(
            response, 'user_index',
            _("You don't have permission to edit this user.")
        )

    def test_delete_user_unauthorized(self):
        response = self.client.post(
            reverse('user_delete', kwargs={'pk': 1}), follow=True
        )
        self.assertRedirectWithMessage(response)
