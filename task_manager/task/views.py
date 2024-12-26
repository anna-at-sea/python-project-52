from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView

from task_manager import utils
from task_manager.task.filters import TaskFilter
from task_manager.task.forms import TaskForm
from task_manager.task.models import Task


class TaskIndexView(utils.UserLoginRequiredMixin, FilterView):
    model = Task
    template_name = 'pages/index_task.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskPageView(utils.UserLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        return render(request, 'pages/page_task.html', context={
            'task': task
        })


class TaskFormCreateView(
    utils.CreateViewMixin, utils.UserLoginRequiredMixin,
    SuccessMessageMixin, CreateView
):
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        task = form.save(commit=False)
        task.creator = self.request.user
        task.save()
        labels = form.cleaned_data.get('labels', [])
        task.labels.set(labels)
        task.save()
        return super().form_valid(form)


class TaskFormUpdateView(
    utils.UpdateViewMixin, utils.UserLoginRequiredMixin,
    SuccessMessageMixin, UpdateView
):
    model = Task
    form_class = TaskForm


class TaskFormDeleteView(
    utils.DeleteViewMixin, utils.UserLoginRequiredMixin,
    SuccessMessageMixin, DeleteView
):
    model = Task

    def dispatch(self, request, *args, **kwargs):
        self.obj = self.get_object()
        if request.user.is_authenticated and self.obj.creator != request.user:
            messages.error(
                request, _("Task can be deleted only by its creator.")
            )
            return redirect('task_index')
        return super().dispatch(request, *args, **kwargs)
