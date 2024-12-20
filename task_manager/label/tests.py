from django.urls import reverse
from django.utils.translation import gettext as _

from task_manager.label.models import Label
from task_manager.status.models import Status
from task_manager.task.models import Task
from task_manager.user.models import User
from task_manager.utils import BaseTestCase


class TestLabelRead(BaseTestCase):
    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_read_label_unauthorized(self):
        response = self.client.get(reverse('label_index'), follow=True)
        self.assertRedirectWithMessage(response)

    def test_read_label_authorized(self):
        self.login_user(self.user)
        response = self.client.get(reverse('label_index'))
        self.assertEqual(response.status_code, 200)


class TestLabelCreate(BaseTestCase):

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
        self.login_user(self.user)
        response = self.client.post(
            reverse('label_create'), self.complete_label_data, follow=True
        )
        label = Label.objects.get(name='complete_label')
        self.assertIsNotNone(label)
        self.assertTrue(Label.objects.filter(name="complete_label").exists())
        self.assertRedirectWithMessage(
            response, 'label_index', _("Label is created successfully")
        )

    def test_create_label_missing_field(self):
        self.login_user(self.user)
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
        self.login_user(self.user)
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
            reverse('label_create'), self.complete_label_data, follow=True
        )
        self.assertRedirectWithMessage(response)


class TestLabelUpdate(BaseTestCase):

    def setUp(self):
        self.label = Label.objects.get(id=1)
        self.user = User.objects.get(id=1)

    def test_update_label_success(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('label_update', kwargs={'pk': 1}),
            {'name': 'new_label'}, follow=True
        )
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'new_label')
        self.assertRedirectWithMessage(
            response, 'label_index', _("Label is updated successfully")
        )

    def test_update_label_missing_field(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('label_update', kwargs={'pk': 1}),
            {'name': ''}
        )
        form = response.context['form']
        self.assertFormError(form, 'name', _('This field is required.'))
        self.assertEqual(response.status_code, 200)

    def test_update_label_unauthorized(self):
        response = self.client.get(
            reverse('label_update', kwargs={'pk': 1}), follow=True
        )
        self.assertRedirectWithMessage(response)


class TestLebelDelete(BaseTestCase):

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.status = Status.objects.get(id=1)
        self.label = Label.objects.get(id=1)
        self.label_in_use = Label.objects.get(id=2)
        self.other_label_in_use = Label.objects.get(id=3)
        self.task = Task.objects.get(id=1)

    def test_delete_label_success(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('label_delete', kwargs={'pk': 1}), follow=True
        )
        self.assertFalse(Label.objects.filter(id=1).exists())
        self.assertRedirectWithMessage(
            response, 'label_index', _("Label is deleted successfully")
        )

    def test_delete_label_unauthorized(self):
        response = self.client.post(
            reverse('label_delete', kwargs={'pk': 1}), follow=True
        )
        self.assertRedirectWithMessage(response)

    def test_delete_label_in_use(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('label_delete', kwargs={'pk': 2}), follow=True
        )
        self.assertTrue(Label.objects.filter(id=2).exists())
        self.assertRedirectWithMessage(
            response, 'label_index',
            _("Cannot delete label while it is being used")
        )
