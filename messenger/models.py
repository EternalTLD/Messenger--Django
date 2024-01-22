from datetime import datetime

from django.db import models
from django.utils import timezone
from django.conf import settings


class Room(models.Model):
    DIRECT = "D"
    GROUP = "G"
    ROOM_TYPE = ((DIRECT, "Direct"), (GROUP, "Group"))

    name = models.CharField(max_length=20, unique=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=False, related_name="room_participants"
    )
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="room_admin",
    )
    room_type = models.CharField(max_length=1, choices=ROOM_TYPE, blank=False)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self) -> str:
        if self.room_type == "D":
            return f"Direct chat room - {self.name}"
        return f"Group chat room - {self.name}"

    @property
    def members_count(self):
        if self.room_type == "D":
            return 2
        return self.participants.count()

    @property
    def get_last_message(self):
        message = Message.objects.filter(room=self).last()
        if message:
            return message.content
        return "There are no messages yet"


class Message(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages"
    )
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, null=True, related_name="messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ["timestamp"]

    def __str__(self) -> str:
        return self.content

    def to_json(self) -> dict:
        return {
            "author": self.author.username,
            "content": self.content,
            "timestamp": datetime.strftime(self.timestamp, "%Y-%m-%d %H:%M"),
        }
