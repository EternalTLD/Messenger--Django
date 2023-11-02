from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("profiles/", include("profiles.urls", namespace="profiles")),
    path("friends/", include("friends.urls", namespace="friends")),
    path("", include("messenger.urls", namespace="messenger")),
]
