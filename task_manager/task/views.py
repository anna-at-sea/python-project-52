from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import UpdateView
from task_manager.task.models import Task
from task_manager.task.forms import TaskForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from .filters import TaskFilter
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied


class TaskIndexView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'task/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')


class TaskPageView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        return render(request, 'task/page.html', context={
            'task': task
        })


class TaskFormCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/create.html'
    success_url = reverse_lazy('task_index')

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')

    def form_valid(self, form):
        task = form.save(commit=False)
        task.creator = self.request.user
        task.save()
        labels = form.cleaned_data.get('labels', [])
        task.labels.set(labels)
        task.save()
        messages.success(self.request, _("Task is created successfully"))
        return super().form_valid(form)


class TaskFormUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/update.html'
    success_url = reverse_lazy('task_index')
    context_object_name = 'task'

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')

    def form_valid(self, form):
        messages.success(self.request, _("Task is updated successfully"))
        return super().form_valid(form)


class TaskFormDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task/delete.html'
    success_url = reverse_lazy('task_index')
    context_object_name = 'task'

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')

    def form_valid(self, form):
        messages.success(self.request, _("Task is deleted successfully"))
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            messages.error(
                request, _("Task can be deleted only by its creator.")
            )
            return redirect('task_index')

    def get_object(self, queryset=None):
        task = super().get_object(queryset)
        if self.request.user.id != task.creator.id:
            raise PermissionDenied
        return task
