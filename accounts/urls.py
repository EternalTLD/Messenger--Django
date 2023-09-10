from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView, 
    PasswordChangeView,
    PasswordChangeDoneView
)

from .views import SignUpView


app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "password_change/", 
        PasswordChangeView.as_view(
            success_url=reverse_lazy('accounts:password_change_done')
        ), 
        name="password_change"
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]