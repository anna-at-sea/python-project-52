from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from task_manager.user.forms import UserForm
from task_manager.user.models import User
from task_manager.utils import UserLoginRequiredMixin


class IndexView(ListView):
    model = User
    template_name = 'pages/user/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


class UserFormCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'pages/user/create.html'
    success_url = reverse_lazy('login')
    success_message = _("User is registered successfully")


class UserFormUpdateView(
    UserLoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = User
    form_class = UserForm
    template_name = 'pages/user/update.html'
    success_url = reverse_lazy('user_index')
    context_object_name = 'form'
    success_message = _("User is updated successfully")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (
            kwargs.get('pk') != request.user.id
        ):
            messages.error(
                request, _("You don't have permission to edit this user.")
            )
            return redirect('user_index')
        return super().dispatch(request, *args, **kwargs)


class UserFormDeleteView(
    UserLoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = User
    template_name = 'pages/user/delete.html'
    success_url = reverse_lazy('user_index')
    context_object_name = 'user'
    success_message = _("User is deleted successfully")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (
            kwargs.get('pk') != request.user.id
        ):
            messages.error(
                request, _("You don't have permission to edit this user.")
            )
            return redirect('user_index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request, _("Cannot delete user while they are in use")
            )
            return redirect('user_index')
