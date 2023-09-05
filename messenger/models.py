from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()

class Room(models.Model):
    name = models.CharField(max_length=20, unique=True)
    participants = models.ManyToManyField(User, blank=False)

    def __str__(self) -> str:
        return self.name

class Message(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'Сообщение от {self.author.username}'
    
    def last_10_messages(self):
        return Message.objects.order_by('-timestamp').all()[:10]