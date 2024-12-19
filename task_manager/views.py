from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView


class IndexView(TemplateView):

    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserLoginView(LoginView):
    template_name = 'pages/login.html'
    redirect_authenticated_user = True

    def get_default_redirect_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("You are logged in")
        )
        return reverse_lazy('index')


class UserLogoutView(LogoutView):
    # template_name = 'pages/logout.html'
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(
            request,
            messages.INFO,
            _("You are logged out")
        )
        return super().dispatch(request, *args, **kwargs)
