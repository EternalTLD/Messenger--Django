from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model


User = get_user_model()

class ProfileDetailView(DetailView):
    template_name = 'profiles/profile_detail.html'
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user'
