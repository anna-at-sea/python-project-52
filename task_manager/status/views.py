from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager import utils
from task_manager.status.forms import StatusForm
from task_manager.status.models import Status


class StatusIndexView(utils.UserLoginRequiredMixin, ListView):
    model = Status
    template_name = 'pages/index_status.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        return context


class StatusFormCreateView(
    utils.CreateViewMixin, utils.UserLoginRequiredMixin,
    SuccessMessageMixin, CreateView
):
    model = Status
    form_class = StatusForm


class StatusFormUpdateView(
    utils.UpdateViewMixin, utils.UserLoginRequiredMixin,
    SuccessMessageMixin, UpdateView
):
    model = Status
    form_class = StatusForm


class StatusFormDeleteView(
    utils.DeleteViewMixin, utils.UserLoginRequiredMixin,
    SuccessMessageMixin, DeleteView
):
    model = Status
