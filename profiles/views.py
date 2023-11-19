from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model
from django.db import transaction

from .forms import UserEditForm, ProfileEditForm
from friends.models import Friend, FriendshipRequest


class ProfileDetailView(DetailView):
    template_name = "profiles/profile_detail.html"
    model = get_user_model()
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
            with transaction.atomic():
                user_form.save()
                profile_form.save()

        return render(
            request,
            self.template_name,
            {"user_form": user_form, "profile_form": profile_form},
        )


def user_search_view(request, *args, **kwargs):
    users = []
    User = get_user_model()

    if request.method == "GET":
        query = request.GET.get("query")
        if query:
            friends = Friend.objects.friends(request.user).values_list(
                "from_user_id", flat=True
            )

            sent_requests = FriendshipRequest.objects.filter(
                from_user=request.user
            ).values_list("to_user_id", flat=True)

            received_requests = FriendshipRequest.objects.filter(
                to_user=request.user
            ).values_list("from_user_id", flat=True)

            search_result = User.objects.filter(username__icontains=query).exclude(
                username=request.user.username
            )
            print(sent_requests, received_requests, friends)

            for user in search_result:
                if user.id not in friends and user.id not in received_requests:
                    sent = user.id in sent_requests
                    users.append((user, sent))

    return render(request, "profiles/search_user.html", {"users": users})
