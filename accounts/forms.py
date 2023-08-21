from typing import Any, Dict
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=25, 
        label='Введите имя пользователя', 
        help_text='Максимальная длинна - 25 символов. Имя не должно сожержать пробелов.'
    )
    email = forms.EmailField(label='Введите email')
    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username):
            raise forms.ValidationError('Пользователь с таким именем уже зарегистрирован.')
        if ' ' in username:
            raise forms.ValidationError('Имя не должно содержать пробелов.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError('Пользователь с таким email адресом уже зарегистрирован.')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли на совпадают.')
        return password2
    
    def save(self, commit=True) -> Any:
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        user.set_password(password)
        if commit:
            user.save()
        return user