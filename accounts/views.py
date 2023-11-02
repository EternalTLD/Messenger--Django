from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model

from .forms import SignUpForm


User = get_user_model()


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "registration/signup.html"

    def post(self, request, *args, **kwargs):
        user_form = SignUpForm(request.POST)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse("accounts:login"))

        return render(request, "registration/signup.html", {"form": user_form})
