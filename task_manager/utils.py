from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _

TRANSLATION_MAP = {
    ('create', 'label'): {
        'success_message': _("Label is created successfully"),
        'heading': _("Create label"),
    },
    ('create', 'status'): {
        'success_message': _("Status is created successfully"),
        'heading': _("Create status"),
    },
    ('create', 'task'): {
        'success_message': _("Task is created successfully"),
        'heading': _("Create task"),
    },
    ('update', 'label'): {
        'success_message': _("Label is updated successfully"),
        'heading': _("Update label"),
    },
    ('update', 'status'): {
        'success_message': _("Status is updated successfully"),
        'heading': _("Update status"),
    },
    ('update', 'task'): {
        'success_message': _("Task is updated successfully"),
        'heading': _("Update task"),
    },
    ('delete', 'label'): {
        'success_message': _("Label is deleted successfully"),
        'heading': _("Delete label"),
    },
    ('delete', 'status'): {
        'success_message': _("Status is deleted successfully"),
        'heading': _("Delete status"),
    },
    ('delete', 'task'): {
        'success_message': _("Task is deleted successfully"),
        'heading': _("Delete task"),
    },
    ('update', 'user'): {
        'success_message': _("User is updated successfully"),
        'heading': _("Update user"),
    },
    ('delete', 'user'): {
        'success_message': _("User is deleted successfully"),
        'heading': _("Delete user"),
    },
    'create': _("Create"),
    'update': _("Update")
}


class BaseTestCase(TestCase):
    fixtures = ["users.json", "tasks.json", "statuses.json", "labels.json"]

    def login_user(self, user):
        self.client.login(
            username=user.username,
            password="correct_password"
        )

    def assertRedirectWithMessage(
        self,
        response,
        redirect_to='login',
        message=_("You are not logged in! Please log in.")
    ):
        self.assertRedirects(response, reverse(redirect_to))
        self.assertTrue(get_messages(response.wsgi_request))
        self.assertContains(response, message)


class UserLoginRequiredMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')


class BaseViewMixin:
    template_name = 'layouts/form_base.html'

    def get_model_name(self):
        return self.model._meta.verbose_name

    def get_success_url(self):
        name = self.get_model_name().lower()
        return reverse_lazy(f'{name}_index')

    def get_success_message(self, *args, **kwargs):
        name = self.get_model_name().lower()
        action = self.get_action().lower()
        translation = (
            TRANSLATION_MAP.get((action, name), {}).get('success_message')
        )
        return translation

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        action = self.get_action().lower()
        name = self.get_model_name().lower()
        context.update({
            'heading': TRANSLATION_MAP.get((action, name), {}).get('heading'),
            'button_text': TRANSLATION_MAP.get(action)
        })
        return context

    def get_action(self):
        raise NotImplementedError


class CreateViewMixin(BaseViewMixin):

    def get_action(self):
        return 'create'


class UpdateViewMixin(BaseViewMixin):

    def get_action(self):
        return 'update'


class DeleteViewMixin(BaseViewMixin):

    def get_action(self):
        return 'delete'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()
        context.update({
            'form': '',
            'delete_prompt': (
                _("Are you sure you want to delete ") + f"{object}?"
            ),
            'button_class': 'btn btn-danger',
            'button_text': _("Yes, delete")
        })
        return context

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except (ValidationError, ProtectedError):
            line_ending = (
                'they are in use' if self.get_model_name().lower() == 'user'
                else 'it is being used'
            )
            name = self.get_model_name().lower()
            messages.error(
                self.request, _(f"Cannot delete {name} while {line_ending}")
            )
            return redirect(f'{name}_index')


class UserPermissionMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (
            kwargs.get('pk') != request.user.id
        ):
            messages.error(
                request, _("You don't have permission to edit this user.")
            )
            return redirect('user_index')
        return super().dispatch(request, *args, **kwargs)
