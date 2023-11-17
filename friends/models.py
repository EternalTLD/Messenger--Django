from django.db import models
from django.db.models import QuerySet
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendship_requests_sent",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendship_requests_received",
    )
    created_at = models.DateTimeField(default=timezone.now)
    rejected_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Friendship request"
        verbose_name_plural = "Friendship requests"
        unique_together = ("from_user", "to_user")

    def __str__(self) -> str:
        return f"Friendship request from {self.from_user} to {self.to_user}"

    def accept(self) -> bool:
        """Accept friendship request"""
        Friend.objects.create(from_user=self.from_user, to_user=self.to_user)
        Friend.objects.create(from_user=self.to_user, to_user=self.from_user)

        # Delete request
        self.delete()

        # Delete cross request
        FriendshipRequest.objects.filter(
            from_user=self.to_user, to_user=self.from_user
        ).delete()
        return True

    def reject(self) -> bool:
        """Reject friendship request"""
        self.rejected_at = timezone.now()
        self.save()
        return True


class FriendshipManager(models.Manager):
    """Friendship manager"""

    def friends(self, user) -> QuerySet:
        """Return a QuerySet of user friends"""
        friends = Friend.objects.filter(to_user=user).select_related("from_user")
        return friends

    def received_requests(self, user) -> QuerySet:
        """Return a QuerySet of friendship requests received by user"""
        requests = FriendshipRequest.objects.filter(to_user=user).select_related(
            "from_user", "to_user"
        )
        return requests

    def sent_requests(self, user) -> QuerySet:
        """Return a QuerySet of friendship requests sent by user"""
        requests = FriendshipRequest.objects.filter(from_user=user).select_related(
            "from_user", "to_user"
        )
        return requests

    def unaccepted_requests(self, user) -> QuerySet:
        """Return a QuerySet of requests that haven't been accepted"""
        requests = FriendshipRequest.objects.filter(
            to_user=user, rejected_at__isnull=True
        ).select_related("from_user", "to_user")
        return requests

    def rejected_requests(self, user) -> QuerySet:
        """Return a QuerySet of friendship requests rejected by user"""
        requests = FriendshipRequest.objects.filter(
            to_user=user,
            rejected_at__isnull=False,
        ).select_related("from_user", "to_user")
        return requests

    def add_friend(self, from_user, to_user) -> FriendshipRequest:
        """Create a friendship request"""
        if from_user == to_user:
            raise ValidationError("You can't send a friendship request to yourself")

        if self.request_already_sent(from_user=from_user, to_user=to_user):
            raise ValidationError("Friendship request has already sent")

        if self.request_already_received(from_user=to_user, to_user=from_user):
            raise ValidationError("Friendship request has already received")

        if self.are_friends(from_user, to_user):
            raise ValidationError(f"Users are already friends")

        request = FriendshipRequest.objects.create(
            from_user=from_user,
            to_user=to_user,
        )
        request.save()
        return request

    def remove_friend(self, from_user, to_user) -> None:
        """Remove friend"""
        return Friend.objects.filter(
            models.Q(from_user=from_user, to_user=to_user)
            | models.Q(from_user=to_user, to_user=from_user)
        ).delete()

    def request_already_sent(self, from_user, to_user) -> bool:
        """Return True if user has already sent request to another user otherwise False"""
        return FriendshipRequest.objects.filter(
            from_user=from_user, to_user=to_user
        ).exists()

    def request_already_received(self, from_user, to_user) -> bool:
        """Return True if user has already received request from another user otherwise False"""
        return FriendshipRequest.objects.filter(
            from_user=to_user, to_user=from_user
        ).exists()

    def are_friends(self, user1, user2) -> bool:
        """Return True if users are friends otherwise False"""
        return Friend.objects.filter(
            models.Q(from_user=user1, to_user=user2)
            | models.Q(from_user=user2, to_user=user1)
        ).exists()


class Friend(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friends",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="_friends",
    )
    created_at = models.DateTimeField(default=timezone.now)

    objects = FriendshipManager()

    class Meta:
        verbose_name = "Friend"
        verbose_name_plural = "Friends"
        unique_together = ("from_user", "to_user")

    def __str__(self) -> str:
        return f"{self.from_user} is friend to {self.to_user}"

    def save(self, *args, **kwargs) -> None:
        if self.from_user == self.to_user:
            raise ValidationError("You can't send a friendship request to yourself")
        return super().save(*args, **kwargs)
