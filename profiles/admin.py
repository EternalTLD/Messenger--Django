from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "country", "city", "status", "last_seen")
    search_fields = ("user__username", "country", "city")
    list_filter = ("last_seen",)
    readonly_fields = ("status", "last_seen")

    def get_queryset(self, request: HttpRequest) -> QuerySet[Profile]:
        qs = super().get_queryset(request)
        return qs.select_related("user")
