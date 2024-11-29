from django.shortcuts import render, redirect
from django.views import View
from task_manager.user.models import User
from task_manager.user.forms import UserForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'user/index.html', context={
            'users': users
        })


class UserFormCreateView(View):

    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, 'user/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _("User is registered successfully")
            )
            return redirect('login')
        return render(request, 'user/create.html', {'form': form})


class UserFormUpdateView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )
        return redirect('login')

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if int(user_id) != request.user.id:
            messages.add_message(
                request,
                messages.ERROR,
                _("You don't have permission to edit this user.")
            )
            return redirect('user_index')
        user = User.objects.get(id=user_id)
        form = UserForm(instance=user)
        return render(
            request,
            'user/update.html',
            {'form': form, 'user_id': user_id}
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if int(user_id) != request.user.id:
            messages.add_message(
                request,
                messages.ERROR,
                _("You don't have permission to edit this user.")
            )
            return redirect('user_index')
        user = User.objects.get(id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _("User is updated successfully")
            )
            return redirect('user_index')
        return render(
            request,
            'user/update.html',
            {'form': form, 'user_id': user_id}
        )


class UserFormDeleteView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )
        return redirect('login')

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if int(user_id) != request.user.id:
            messages.add_message(
                request,
                messages.ERROR,
                _("You don't have permission to edit this user.")
            )
            return redirect('user_index')
        user = User.objects.get(id=user_id)
        return render(
            request,
            'user/delete.html',
            {'user': user}
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if int(user_id) != request.user.id:
            messages.add_message(
                request,
                messages.ERROR,
                _("You don't have permission to edit this user.")
            )
            return redirect('user_index')
        user = User.objects.get(id=user_id)
        if user:
            user.delete()
            messages.add_message(
                request,
                messages.SUCCESS,
                _("User is deleted successfully"))
        return redirect('user_index')
