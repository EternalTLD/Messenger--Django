from django import forms
from django.contrib.auth import get_user_model

from .models import Profile


User = get_user_model()

class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'