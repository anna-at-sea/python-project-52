from django.shortcuts import render, redirect
from django.views import View
from task_manager.task.models import Task
from task_manager.user.models import User
from task_manager.status.models import Status
from task_manager.label.models import Label
from task_manager.task.forms import TaskForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin


class TaskIndexView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )
        return redirect('login')

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        labels = Label.objects.all()
        users = User.objects.all()
        status_filter = request.GET.get('status')
        executor_filter = request.GET.get('executor')
        choice_filter = request.GET.get('choice')
        label_filter = request.GET.getlist('label')
        tasks = Task.objects.all()
        if status_filter:
            tasks = tasks.filter(status_id=status_filter)
        if executor_filter:
            tasks = tasks.filter(executor_id=executor_filter)
        if choice_filter:
            tasks = tasks.filter(creator_id=request.user.id)
        if label_filter:
            tasks = tasks.filter(labels__id__in=label_filter).distinct()
        return render(request, 'task/index.html', context={
            'tasks': tasks, 'statuses': statuses, 'users': users,
            'labels': labels,
            'status_filter': status_filter, 'executor_filter': executor_filter,
            'choice_filter': choice_filter, 'label_filter': label_filter
        })


class TaskPageView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )
        return redirect('login')

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        return render(request, 'task/page.html', context={
            'task': task
        })


class TaskFormCreateView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )
        return redirect('login')

    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, 'task/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            labels = form.cleaned_data['labels']
            task.labels.set(labels)
            task.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _("Task is created successfully")
            )
            return redirect('task_index')
        return render(request, 'task/create.html', {'form': form})


class TaskFormUpdateView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )
        return redirect('login')

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        form = TaskForm(instance=task)
        return render(
            request,
            'task/update.html',
            {'form': form, 'task_id': task_id}
        )

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _("Task is updated successfully")
            )
            return redirect('task_index')
        return render(
            request,
            'task/update.html',
            {'form': form, 'task_id': task_id}
        )


class TaskFormDeleteView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )
        return redirect('login')

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        if task.creator_id != request.user.id:
            messages.add_message(
                request,
                messages.ERROR,
                _("Task can be deleted only by its creator.")
            )
            return redirect('task_index')
        return render(
            request,
            'task/delete.html',
            {'task': task}
        )

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        if task.creator_id != request.user.id:
            messages.add_message(
                request,
                messages.ERROR,
                _("Task can be deleted only by its creator.")
            )
        else:
            task.delete()
            messages.add_message(
                request,
                messages.SUCCESS,
                _("Task is deleted successfully"))
        return redirect('task_index')
