from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='avatars/%Y/%m/%d/', blank=True, null=True,)
    phone = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=25, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    bio = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.user} profile'
    
class FriendRequest(models.Model):
    user_from = models.ForeignKey(User)
    user_to = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField()

