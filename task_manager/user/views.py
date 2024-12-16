from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import UpdateView
from task_manager.user.models import User
from task_manager.user.forms import UserForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError


class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'user/index.html', context={
            'users': users
        })


class UserFormCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("User is registered successfully"))
        return response


class UserFormUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/update.html'
    success_url = reverse_lazy('user_index')
    context_object_name = 'form'

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            messages.error(
                request, _("You don't have permission to edit this user.")
            )
            return redirect('user_index')

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        if user.id != self.request.user.id:
            raise PermissionDenied
        return user

    def form_valid(self, form):
        messages.success(self.request, _("User is updated successfully"))
        return super().form_valid(form)


class UserFormDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user_index')
    context_object_name = 'user'

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            messages.error(
                request, _("You don't have permission to edit this user.")
            )
            return redirect('user_index')

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        if user.id != self.request.user.id:
            raise PermissionDenied
        return user

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, _("User is deleted successfully"))
        except ProtectedError:
            messages.error(
                self.request, _("Cannot delete user while they are in use")
            )
        return redirect('user_index')
