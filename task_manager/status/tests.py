from django.urls import reverse
from django.utils.translation import gettext as _

from task_manager.status.models import Status
from task_manager.user.models import User
from task_manager.utils import BaseTestCase


class TestStatusRead(BaseTestCase):

    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_read_status_unauthorized(self):
        response = self.client.get(reverse('status_index'), follow=True)
        self.assertRedirectWithMessage(response)

    def test_read_status_authorized(self):
        self.login_user(self.user)
        response = self.client.get(reverse('status_index'))
        self.assertEqual(response.status_code, 200)


class TestStatusCreate(BaseTestCase):

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
        self.login_user(self.user)
        response = self.client.post(
            reverse('status_create'), self.complete_status_data, follow=True
        )
        status = Status.objects.get(name='complete_status')
        self.assertIsNotNone(status)
        self.assertTrue(Status.objects.filter(name="complete_status").exists())
        self.assertRedirectWithMessage(
            response, 'status_index', _("Status is created successfully")
        )

    def test_create_status_missing_field(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('status_create'), self.missing_field_status_data
        )
        form = response.context['form']
        self.assertFormError(form, 'name', _('This field is required.'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Status.objects.filter(name="").exists()
        )

    def test_create_duplicate_status(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('status_create'), self.duplicate_status_data
        )
        form = response.context['form']
        self.assertFormError(
            form, 'name', _('Task status with this name already exists.')
        )
        self.assertEqual(response.status_code, 200)

    def test_create_status_unauthorized(self):
        response = self.client.post(
            reverse('status_create'), self.complete_status_data, follow=True
        )
        self.assertRedirectWithMessage(response)


class TestStatusUpdate(BaseTestCase):

    def setUp(self):
        self.status = Status.objects.get(id=1)
        self.user = User.objects.get(id=1)

    def test_update_status_success(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('status_update', kwargs={'pk': 1}),
            {'name': 'new_status'}, follow=True
        )
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'new_status')
        self.assertRedirectWithMessage(
            response, 'status_index', _("Status is updated successfully")
        )

    def test_update_status_missing_field(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('status_update', kwargs={'pk': 1}),
            {'name': ''}
        )
        form = response.context['form']
        self.assertFormError(form, 'name', _('This field is required.'))
        self.assertEqual(response.status_code, 200)

    def test_update_status_unauthorized(self):
        response = self.client.get(
            reverse('status_update', kwargs={'pk': 1}), follow=True
        )
        self.assertRedirectWithMessage(response)


class TestStatusDelete(BaseTestCase):

    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_delete_status_success(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('status_delete', kwargs={'pk': 1}), follow=True
        )
        self.assertFalse(Status.objects.filter(id=1).exists())
        self.assertRedirectWithMessage(
            response, 'status_index', _("Status is deleted successfully")
        )

    def test_delete_status_unauthorized(self):
        response = self.client.post(
            reverse('status_delete', kwargs={'pk': 1}), follow=True
        )
        self.assertRedirectWithMessage(response)

    def test_delete_status_in_use(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('status_delete', kwargs={'pk': 2}), follow=True
        )
        self.assertTrue(Status.objects.filter(id=2).exists())
        self.assertRedirectWithMessage(
            response, 'status_index',
            _("Cannot delete status while it is being used")
        )
