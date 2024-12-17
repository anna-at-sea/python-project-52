from os.path import join

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _
from task_manager.status.models import Status
from task_manager.task.models import Task
from task_manager.user.models import User

from .models import Label

USERS_FIXTURE_PATH = 'task_manager/user/fixtures/'
TASKS_FIXTURE_PATH = 'task_manager/task/fixtures/'
STATUSES_FIXTURE_PATH = 'task_manager/status/fixtures/'


class TestLabelRead(TestCase):
    fixtures = [join(USERS_FIXTURE_PATH, "users.json")]

    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_read_label_unauthorized(self):
        response = self.client.get(reverse('label_index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(
            str(messages[0]),
            _("You are not logged in! Please log in.")
        )

    def test_read_label_authorized(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.get(reverse('label_index'))
        self.assertEqual(response.status_code, 200)


class TestLabelCreate(TestCase):
    fixtures = [join(USERS_FIXTURE_PATH, "users.json"), "labels.json"]

    def setUp(self):
        self.complete_label_data = {
            'name': 'complete_label'
        }
        self.missing_field_label_data = {
            'name': ''
        }
        self.label = Label.objects.get(id=1)
        self.user = User.objects.get(id=1)
        self.duplicate_label_data = {
            'name': 'testlabel'
        }

    def test_create_label_success(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(
            reverse('label_create'), self.complete_label_data
        )
        self.assertEqual(response.status_code, 302)
        label = Label.objects.get(name='complete_label')
        self.assertIsNotNone(label)
        self.assertTrue(Label.objects.filter(name="complete_label").exists())

    def test_create_label_missing_field(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(
            reverse('label_create'), self.missing_field_label_data
        )
        form = response.context['form']
        self.assertFormError(form, 'name', _('This field is required.'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Label.objects.filter(name="").exists()
        )

    def test_create_duplicate_label(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(
            reverse('label_create'), self.duplicate_label_data
        )
        form = response.context['form']
        self.assertFormError(
            form, 'name', _('Label with this name already exists.')
        )
        self.assertEqual(response.status_code, 200)

    def test_create_label_unauthorized(self):
        response = self.client.post(
            reverse('label_create'), self.complete_label_data
        )
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(
            str(messages[0]),
            _("You are not logged in! Please log in.")
        )


class TestLabelUpdate(TestCase):
    fixtures = [join(USERS_FIXTURE_PATH, "users.json"), "labels.json"]

    def setUp(self):
        self.label = Label.objects.get(id=1)
        self.user = User.objects.get(id=1)

    def test_update_label_success(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(
            reverse('label_update', kwargs={'pk': 1}),
            {'name': 'new_label'}
        )
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'new_label')

    def test_update_label_missing_field(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(
            reverse('label_update', kwargs={'pk': 1}),
            {'name': ''}
        )
        form = response.context['form']
        self.assertFormError(form, 'name', _('This field is required.'))
        self.assertEqual(response.status_code, 200)

    def test_update_label_unauthorized(self):
        response = self.client.get(reverse('label_update', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(
            str(messages[0]),
            _("You are not logged in! Please log in.")
        )


class TestLebelDelete(TestCase):
    fixtures = [
        join(USERS_FIXTURE_PATH, "users.json"),
        join(TASKS_FIXTURE_PATH, "tasks.json"),
        join(STATUSES_FIXTURE_PATH, "statuses.json"),
        "labels.json"
    ]

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.status = Status.objects.get(id=1)
        self.label = Label.objects.get(id=1)
        self.label_in_use = Label.objects.get(id=2)
        self.other_label_in_use = Label.objects.get(id=3)
        self.task = Task.objects.get(id=1)

    def test_delete_label_success(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(reverse('label_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_index'))
        self.assertFalse(Label.objects.filter(id=1).exists())

    def test_delete_label_unauthorized(self):
        response = self.client.post(reverse('label_delete', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(
            str(messages[0]),
            _("You are not logged in! Please log in.")
        )

    def test_delete_label_in_use(self):
        self.client.login(
            username=self.user.username,
            password="correct_password"
        )
        response = self.client.post(reverse('label_delete', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_index'))
        self.assertTrue(Label.objects.filter(id=2).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(
            str(messages[0]),
            _("Cannot delete label while it is being used")
        )
