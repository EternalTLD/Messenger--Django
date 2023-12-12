from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache


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
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user} profile"

    @property
    def is_online(self) -> bool:
        cache_key = f"last_activity_{self.user.id}"
        last_seen = cache.get(cache_key)
        if last_seen is not None and timezone.now() - last_seen < timezone.timedelta(
            seconds=300
        ):
            return True
        return False

    @property
    def status(self) -> str:
        if self.is_online:
            return "Online"
        return "Offline"
