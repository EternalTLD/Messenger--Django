from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model

from .forms import UserEditForm, ProfileEditForm


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
        user_form = self.user_form(instance=request.user)
        profile_form = self.profile_form(instance=request.user.profile)
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        user_form = self.user_form(instance=request.user, 
                                   data=request.POST)
        profile_form = self.profile_form(instance=request.user.profile,
                                         data=request.POST,
                                         files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})