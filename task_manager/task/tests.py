from django.test import TestCase, RequestFactory
from task_manager.status.models import Status
from task_manager.user.models import User
from task_manager.task.models import Task
from task_manager.task.filters import TaskFilter
from task_manager.task.views import TaskIndexView
from task_manager.label.models import Label
from django.urls import reverse
from django.contrib.messages import get_messages
from os.path import join


USERS_FIXTURE_PATH = 'task_manager/user/fixtures/'
STATUSES_FIXTURE_PATH = 'task_manager/status/fixtures/'
LABELS_FIXTURE_PATH = 'task_manager/label/fixtures/'


class BaseTaskTestCase(TestCase):
    fixtures = [
        join(USERS_FIXTURE_PATH, "users.json"),
        join(STATUSES_FIXTURE_PATH, "statuses.json"),
        join(LABELS_FIXTURE_PATH, "labels.json"),
        "tasks.json"
    ]

    def login_user(self, user):
        self.client.login(
            username=user.username,
            password="correct_password"
        )

    def assertRedirectLogin(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(
            str(messages[0]),
            "You are not logged in! Please log in."
        )


class TestTaskRead(BaseTaskTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.get(id=1)

    def test_read_task_index_unauthorized(self):
        response = self.client.get(reverse('task_index'))
        self.assertRedirectLogin(response)

    def test_read_task_page_unauthorized(self):
        response = self.client.get(reverse('task_page', kwargs={'pk': 1}))
        self.assertRedirectLogin(response)

    def test_read_task_authorized(self):
        self.login_user(self.user)
        response = self.client.get(reverse('task_index'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('task_page', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)


class TestTaskCreate(BaseTaskTestCase):
    def setUp(self):
        super().setUp()
        self.status = Status.objects.get(id=1)
        self.user = User.objects.get(id=1)
        self.task = Task.objects.get(id=1)
        self.label1 = Label.objects.get(id=1)
        self.label2 = Label.objects.get(id=2)
        self.complete_task_data = {
            'name': 'complete_task',
            'creator': self.user.id,
            'status': self.status.id
        }
        self.full_task_data = {
            'name': 'full_task',
            'description': 'this is task description',
            'creator': self.user.id,
            'status': self.status.id,
            'executor': self.user.id,
            'labels': [self.label1.id, self.label2.id]
        }
        self.missing_field_task_data = {
            'name': 'missing_field_task',
            'creator': self.user.id
        }
        self.duplicate_task_data = {
            'name': 'testtask',
            'creator': self.user.id,
            'status': self.status.id
        }

    def test_create_task_success(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('task_create'), self.complete_task_data
        )
        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(name='complete_task')
        self.assertIsNotNone(task)
        self.assertTrue(Task.objects.filter(name="complete_task").exists())
        self.assertEqual(task.creator, self.user)

    def test_create_full_task_success(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('task_create'), self.full_task_data
        )
        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(name='full_task')
        self.assertIsNotNone(task)
        self.assertTrue(Task.objects.filter(name="full_task").exists())
        labels = task.labels.all()
        self.assertIn(self.label1, labels)
        self.assertIn(self.label2, labels)
        self.assertEqual(labels.count(), 2)

    def test_create_task_missing_field(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('task_create'), self.missing_field_task_data
        )
        form = response.context['form']
        self.assertFormError(form, 'status', 'This field is required.')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Task.objects.filter(name="missing_field_task").exists()
        )

    def test_create_duplicate_task(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('task_create'), self.duplicate_task_data
        )
        form = response.context['form']
        self.assertFormError(
            form, 'name', 'Task with this name already exists.'
        )
        self.assertEqual(response.status_code, 200)

    def test_create_task_unauthorized(self):
        response = self.client.post(
            reverse('task_create'), self.complete_task_data
        )
        self.assertRedirectLogin(response)


class TestTaskUpdate(BaseTaskTestCase):
    def setUp(self):
        super().setUp()
        self.task = Task.objects.get(id=1)
        self.user = User.objects.get(id=1)
        self.updated_task_data = {
            'name': 'new_task',
            'description': 'new_description',
            'creator': self.task.creator.id,
            'status': self.task.status.id
        }

    def test_update_task_success(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('task_update', kwargs={'pk': 1}),
            self.updated_task_data
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'new_task')
        self.assertEqual(self.task.description, 'new_description')

    def test_update_task_missing_field(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse('task_update', kwargs={'pk': 1}),
            {'name': ''}
        )
        form = response.context['form']
        self.assertFormError(form, 'name', 'This field is required.')
        self.assertEqual(response.status_code, 200)

    def test_update_task_unauthorized(self):
        response = self.client.get(reverse('task_update', kwargs={'pk': 1}))
        self.assertRedirectLogin(response)


class TestTaskDelete(BaseTaskTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.get(id=1)
        self.other_user = User.objects.get(id=2)
        self.task = Task.objects.get(id=1)

    def test_delete_task_success(self):
        self.login_user(self.user)
        response = self.client.post(reverse('task_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_index'))
        self.assertFalse(Task.objects.filter(id=1).exists())

    def test_delete_task_of_other_user(self):
        self.login_user(self.other_user)
        response = self.client.get(reverse('task_delete', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('task_index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(
            str(messages[0]),
            "Task can be deleted only by its creator."
        )

    def test_delete_task_unauthorized(self):
        response = self.client.post(reverse('task_delete', kwargs={'pk': 1}))
        self.assertRedirectLogin(response)


class TestTaskFilter(BaseTaskTestCase):
    def setUp(self):
        super().setUp()
        self.status1 = Status.objects.get(id=1)
        self.status2 = Status.objects.get(id=2)
        self.executor = User.objects.get(id=2)
        self.label1 = Label.objects.get(id=1)
        self.label2 = Label.objects.get(id=2)
        self.label3 = Label.objects.get(id=3)
        self.user = User.objects.get(id=1)
        self.factory = RequestFactory()

    def test_status_filter(self):
        request = self.factory.get(
            reverse('task_index'),
            {'status': self.status2.id}
        )
        request.user = self.user
        response = TaskIndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "task1")
        self.assertContains(response, "testtask")
        filtered_tasks = response.context_data['object_list']
        self.assertEqual(len(filtered_tasks), 1)
        request2 = self.factory.get(
            reverse('task_index'),
            {'status': self.status1.id}
        )
        request2.user = self.user
        response = TaskIndexView.as_view()(request2)
        self.assertEqual(response.status_code, 200)
        filtered_tasks = response.context_data['object_list']
        self.assertEqual(len(filtered_tasks), 0)

    def test_executor_filter(self):
        request = self.factory.get(
            reverse('task_index'),
            {'executor': self.executor.id}
        )
        request.user = self.user
        response = TaskIndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "task1")
        self.assertNotContains(response, "testtask")
        filtered_tasks = response.context_data['object_list']
        self.assertEqual(len(filtered_tasks), 1)
        request2 = self.factory.get(
            reverse('task_index'),
            {'executor': self.user.id}
        )
        request2.user = self.user
        response = TaskIndexView.as_view()(request2)
        self.assertEqual(response.status_code, 200)
        filtered_tasks = response.context_data['object_list']
        self.assertEqual(len(filtered_tasks), 0)

    def test_labels_filter(self):
        request = self.factory.get(
            reverse('task_index'),
            {'labels': [self.label2.id]}
        )
        request.user = self.user
        response = TaskIndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "task1")
        self.assertContains(response, "testtask")
        filtered_tasks = response.context_data['object_list']
        self.assertEqual(len(filtered_tasks), 2)
        request2 = self.factory.get(
            reverse('task_index'),
            {'labels': [self.label2.id, self.label3.id]}
        )
        request2.user = self.user
        response = TaskIndexView.as_view()(request2)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testtask")
        self.assertContains(response, "task1")
        request3 = self.factory.get(
            reverse('task_index'), {'labels': [self.label1.id]}
        )
        request3.user = self.user
        response = TaskIndexView.as_view()(request3)
        self.assertEqual(response.status_code, 200)
        filtered_tasks = response.context_data['object_list']
        self.assertEqual(len(filtered_tasks), 0)

    def test_created_by_me_filter(self):
        request = self.factory.get(
            reverse('task_index'), {'created_by_me': 'on'}
        )
        request.user = self.user
        response = TaskIndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testtask")
        self.assertNotContains(response, "task1")
        filtered_tasks = response.context_data['object_list']
        self.assertEqual(len(filtered_tasks), 1)
        request2 = self.factory.get(reverse('task_index'))
        request2.user = self.user
        response = TaskIndexView.as_view()(request2)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testtask")
        self.assertContains(response, "task1")
        filtered_tasks = response.context_data['object_list']
        self.assertEqual(len(filtered_tasks), 2)
