from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView, DeleteView
from django_filters.views import FilterView

from task_manager.utils import UserLoginRequiredMixin
from task_manager.task.filters import TaskFilter
from task_manager.task.forms import TaskForm
from task_manager.task.models import Task


class TaskIndexView(UserLoginRequiredMixin, FilterView):
    model = Task
    template_name = 'pages/task/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskPageView(UserLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        return render(request, 'pages/task/page.html', context={
            'task': task
        })


class TaskFormCreateView(
    UserLoginRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Task
    form_class = TaskForm
    template_name = 'pages/task/create.html'
    success_url = reverse_lazy('task_index')
    success_message = _("Task is created successfully")

    def form_valid(self, form):
        task = form.save(commit=False)
        task.creator = self.request.user
        task.save()
        labels = form.cleaned_data.get('labels', [])
        task.labels.set(labels)
        task.save()
        return super().form_valid(form)


class TaskFormUpdateView(
    UserLoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Task
    form_class = TaskForm
    template_name = 'pages/task/update.html'
    success_url = reverse_lazy('task_index')
    context_object_name = 'task'
    success_message = _("Task is updated successfully")


class TaskFormDeleteView(
    UserLoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Task
    template_name = 'pages/task/delete.html'
    success_url = reverse_lazy('task_index')
    context_object_name = 'task'
    success_message = _("Task is deleted successfully")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (
            kwargs.get('pk') not in
            request.user.created_tasks.values_list('id', flat=True)
        ):
            messages.error(
                request, _("Task can be deleted only by its creator.")
            )
            return redirect('task_index')
        return super().dispatch(request, *args, **kwargs)
