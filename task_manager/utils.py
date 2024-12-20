from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import get_messages
from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _


class BaseTestCase(TestCase):
    fixtures = ["users.json", "tasks.json", "statuses.json", "labels.json"]

    def login_user(self, user):
        self.client.login(
            username=user.username,
            password="correct_password"
        )

    def assertRedirectWithMessage(
        self,
        response,
        redirect_to='login',
        message=_("You are not logged in! Please log in.")
    ):
        self.assertRedirects(response, reverse(redirect_to))
        self.assertTrue(get_messages(response.wsgi_request))
        self.assertContains(response, message)


class UserLoginRequiredMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')
