from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from task_manager.utils import UserLoginRequiredMixin
from task_manager.status.forms import StatusForm
from task_manager.status.models import Status


class StatusIndexView(UserLoginRequiredMixin, ListView):
    model = Status
    template_name = 'pages/status/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        return context


class StatusFormCreateView(
    UserLoginRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Status
    form_class = StatusForm
    template_name = 'pages/status/create.html'
    success_url = reverse_lazy('status_index')
    success_message = _("Status is created successfully")


class StatusFormUpdateView(
    UserLoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Status
    form_class = StatusForm
    template_name = 'pages/status/update.html'
    success_url = reverse_lazy('status_index')
    context_object_name = 'status'
    success_message = _("Status is updated successfully")


class StatusFormDeleteView(
    UserLoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Status
    template_name = 'pages/status/delete.html'
    success_url = reverse_lazy('status_index')
    context_object_name = 'status'
    success_message = _("Status is deleted successfully")

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request, _("Cannot delete status while it is being used")
            )
            return redirect('status_index')
