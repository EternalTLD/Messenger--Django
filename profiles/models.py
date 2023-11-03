from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    profile_image = models.ImageField(
        upload_to="avatars/%Y/%m/%d/",
        blank=True,
        null=True,
    )
    phone = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=25, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    bio = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user} profile"
