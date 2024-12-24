from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.status.forms import StatusForm
from task_manager.status.models import Status
from task_manager.utils import CreateViewMixin, DeleteViewMixin, \
    UpdateViewMixin, UserLoginRequiredMixin


class StatusIndexView(UserLoginRequiredMixin, ListView):
    model = Status
    template_name = 'pages/index_status.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        return context


class StatusFormCreateView(
    CreateViewMixin, UserLoginRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Status
    form_class = StatusForm


class StatusFormUpdateView(
    UpdateViewMixin, UserLoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Status
    form_class = StatusForm


class StatusFormDeleteView(
    DeleteViewMixin, UserLoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Status
