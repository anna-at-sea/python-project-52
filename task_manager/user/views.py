from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.user.forms import UserForm
from task_manager.user.models import User
from task_manager.utils import (
    CreateViewMixin, DeleteViewMixin, UpdateViewMixin,
    UserLoginRequiredMixin, UserPermissionMixin
)


class IndexView(ListView):
    model = User
    template_name = 'pages/index_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


class UserFormCreateView(CreateViewMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm

    def get_success_message(self, *args, **kwargs):
        return _("User is registered successfully")

    def get_success_url(self):
        return reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'heading': _("Registration"),
            'button_text': _("Register")
        })
        return context


class UserFormUpdateView(
    UpdateViewMixin, UserLoginRequiredMixin, UserPermissionMixin,
    SuccessMessageMixin, UpdateView
):
    model = User
    form_class = UserForm


class UserFormDeleteView(
    DeleteViewMixin, UserLoginRequiredMixin, UserPermissionMixin,
    SuccessMessageMixin, DeleteView
):
    model = User
