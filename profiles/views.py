from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model

from .forms import UserEditForm, ProfileEditForm
from friends.models import Friend


User = get_user_model()

class ProfileDetailView(DetailView):
    template_name = 'profiles/profile_detail.html'
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user'

class ProfileEditView(View):
    user_form = UserEditForm
    profile_form = ProfileEditForm
    template_name = 'profiles/profile_edit.html'

    def get(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        context = {'user_form': user_form, 'profile_form': profile_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user, 
                                   data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                         data=request.POST,
                                         files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        context = {'user_form': user_form, 'profile_form': profile_form}
        return render(request, 'profiles/profile_edit.html', context)
    
def user_search_view(request, *args, **kwargs):
    users = []

    if request.method == 'GET':
        query = request.GET.get('query')
        auth_user = request.user
        search_result = User.objects.filter(username__icontains=query).exclude(username=auth_user.username)
        for user in search_result:
            if not Friend.objects.are_friends(user, auth_user):
                users.append(user)

    return render(request, 'profiles/search_user.html', {'users': users})
