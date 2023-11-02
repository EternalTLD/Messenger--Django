from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils import timezone
from django.conf import settings


class FriendshipManager(models.Manager):
    """Friendship manager"""

    def friends(self, user):
        """Return a list of user friends"""
        friends = Friend.objects.select_related("from_user").filter(to_user=user)
        return friends

    def requests(self, user):
        """Return a list of user friendship requests"""
        requests = FriendshipRequest.objects.filter(to_user=user).select_related(
            "from_user", "to_user"
        )
        return requests

    def sent_requests(self, user):
        """Return a list of friendship requests sent by user"""
        requests = FriendshipRequest.objects.filter(from_user=user).select_related(
            "from_user", "to_user"
        )
        return requests

    def unaccepted_requests(self, user):
        """Return a list of requests that haven't been accepted"""
        requests = FriendshipRequest.objects.filter(
            to_user=user, rejected_at__isnull=True
        ).select_related("from_user", "to_user")
        return requests

    def rejected_requests(self, user):
        """Return a list of user rejected friendship requests"""
        requests = FriendshipRequest.objects.filter(
            to_user=user,
            rejected_at__isnull=False,
        ).select_related("from_user", "to_user")
        return requests

    def add_friend(self, from_user, to_user, message=""):
        """Create a friendship request"""
        if from_user == to_user:
            raise ValidationError("You can't send a friendship request to yourself")

        if FriendshipRequest.objects.filter(
            from_user=from_user, to_user=to_user
        ).exists():
            raise ValidationError("Friendship request has already sent")

        if FriendshipRequest.objects.filter(from_user=to_user, to_user=from_user):
            raise ValidationError("User has alredy sent a freindship request to you")

        if self.are_friends(from_user, to_user):
            raise ValidationError(f"You and {to_user.username} are already friends")

        request = FriendshipRequest.objects.create(
            from_user=from_user,
            to_user=to_user,
        )
        request.save()
        return request

    def remove_friend(self, from_user, to_user):
        """Remove friend"""
        try:
            friend = Friend.objects.filter(
                from_user__in=[from_user, to_user], to_user__in=[from_user, to_user]
            )
            if friend:
                friend.delete()
                return True

        except ObjectDoesNotExist:
            return False

    def are_friends(self, user1, user2):
        try:
            friend = Friend.objects.filter(
                from_user__in=[user1, user2], to_user__in=[user1, user2]
            )
            if friend:
                return True

        except ObjectDoesNotExist:
            return False


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


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendship_requests_sent",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendship_requests_recived",
    )
    created_at = models.DateTimeField(default=timezone.now)
    rejected_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Friendship request"
        verbose_name_plural = "Friendship requests"
        unique_together = ("from_user", "to_user")

    def __str__(self) -> str:
        return f"Friendship request from {self.from_user} to {self.to_user}"

    def accept(self):
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

    def reject(self):
        """Reject friendship request"""
        self.rejected_at = timezone.now()
        self.save()
        return True
