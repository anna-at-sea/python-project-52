from django.test import TestCase
from task_manager.status.models import Status
from task_manager.user.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from os.path import join


USERS_FIXTURE_PATH = 'task_manager/user/fixtures/'


class TestStatusRead(TestCase):
    fixtures = [join(USERS_FIXTURE_PATH, "users.json")]

    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_read_status_unauthorized(self):
        response = self.client.get(reverse('status_index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(
            str(messages[0]),
            "You are not logged in! Please log in."
        )

    def test_read_status_authorized(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.get(reverse('status_index'))
        self.assertEqual(response.status_code, 200)


class TestStatusCreate(TestCase):
    fixtures = [join(USERS_FIXTURE_PATH, "users.json"), "statuses.json"]

    def setUp(self):
        self.complete_status_data = {
            'name': 'complete_status'
        }
        self.missing_field_status_data = {
            'name': ''
        }
        self.status = Status.objects.get(id=1)
        self.user = User.objects.get(id=1)
        self.duplicate_status_data = {
            'name': 'teststatus'
        }

    def test_create_status_success(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(
            reverse('status_create'), self.complete_status_data
        )
        self.assertEqual(response.status_code, 302)
        status = Status.objects.get(name='complete_status')
        self.assertIsNotNone(status)
        self.assertTrue(Status.objects.filter(name="complete_status").exists())

    def test_create_status_missing_field(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(
            reverse('status_create'), self.missing_field_status_data
        )
        form = response.context['form']
        self.assertFormError(form, 'name', 'This field is required.')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Status.objects.filter(name="").exists()
        )

    def test_create_duplicate_status(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(
            reverse('status_create'), self.duplicate_status_data
        )
        print(response)
        form = response.context['form']
        self.assertFormError(
            form, 'name', 'Task status with this name already exists.'
        )
        self.assertEqual(response.status_code, 200)

    def test_create_status_unauthorized(self):
        response = self.client.post(
            reverse('status_create'), self.complete_status_data
        )
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(
            str(messages[0]),
            "You are not logged in! Please log in."
        )


class TestStatusUpdate(TestCase):
    fixtures = [join(USERS_FIXTURE_PATH, "users.json"), "statuses.json"]

    def setUp(self):
        self.status = Status.objects.get(id=1)
        self.user = User.objects.get(id=1)

    def test_update_status_success(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(
            reverse('status_update', kwargs={'id': 1}),
            {'name': 'new_status'}
        )
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'new_status')

    def test_update_status_missing_field(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(
            reverse('status_update', kwargs={'id': 1}),
            {'name': ''}
        )
        form = response.context['form']
        self.assertFormError(form, 'name', 'This field is required.')
        self.assertEqual(response.status_code, 200)

    def test_update_status_unauthorized(self):
        response = self.client.get(reverse('status_update', kwargs={'id': 1}))
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(
            str(messages[0]),
            "You are not logged in! Please log in."
        )


class TestStatusDelete(TestCase):
    fixtures = [join(USERS_FIXTURE_PATH, "users.json"), "statuses.json"]

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.status = Status.objects.get(id=1)

    def test_delete_status_success(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(reverse('status_delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_index'))
        self.assertFalse(Status.objects.filter(id=1).exists())

    def test_delete_status_unauthorized(self):
        response = self.client.post(reverse('status_delete', kwargs={'id': 1}))
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(
            str(messages[0]),
            "You are not logged in! Please log in."
        )
