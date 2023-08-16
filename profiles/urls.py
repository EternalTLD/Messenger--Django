from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
    path('edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('<slug:username>/', views.ProfileDetailView.as_view(), name='profile_detail'),
]