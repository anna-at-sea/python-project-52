from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager import utils
from task_manager.label.forms import LabelForm
from task_manager.label.models import Label


class LabelIndexView(utils.UserLoginRequiredMixin, ListView):
    model = Label
    template_name = 'pages/index_label.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = Label.objects.all()
        return context


class LabelFormCreateView(
    utils.CreateViewMixin, utils.UserLoginRequiredMixin,
    SuccessMessageMixin, CreateView
):
    model = Label
    form_class = LabelForm


class LabelFormUpdateView(
    utils.UpdateViewMixin, utils.UserLoginRequiredMixin,
    SuccessMessageMixin, UpdateView
):
    model = Label
    form_class = LabelForm


class LabelFormDeleteView(
    utils.DeleteViewMixin, utils.UserLoginRequiredMixin,
    SuccessMessageMixin, DeleteView
):
    model = Label
