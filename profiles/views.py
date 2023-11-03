from typing import Any
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model

from .forms import UserEditForm, ProfileEditForm
from friends.models import Friend


User = get_user_model()


class ProfileDetailView(DetailView):
    template_name = "profiles/profile_detail.html"
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "user"


class ProfileEditView(View):
    user_form = UserEditForm
    profile_form = ProfileEditForm
    template_name = "profiles/profile_edit.html"

    def get(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        return render(
            request,
            self.template_name,
            {"user_form": user_form, "profile_form": profile_form},
        )

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

        return render(
            request,
            "profiles/profile_edit.html",
            {"user_form": user_form, "profile_form": profile_form},
        )


def user_search_view(request, *args, **kwargs):
    users = []
    current_user = request.user

    if request.method == "GET":
        query = request.GET.get("query")
        if query:
            search_result = User.objects.filter(username__icontains=query).exclude(
                username=current_user.username
            )
            for user in search_result:
                if not Friend.objects.are_friends(user, current_user):
                    users.append(user)

    return render(request, "profiles/search_user.html", {"users": users})
