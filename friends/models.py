from typing import Iterable, Optional
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

User = get_user_model()

class FriendshipManager(models.Manager):
    """Friendship manager"""

    def friends(self, user):
        """Return a list of user friends"""
        qs = Friend.objects.select_related('from_user').filter(to_user=user)
        friends = list(qs)
        return friends
    
    def requests(self, user):
        """Return a list of user friendship requests"""
        qs = FriendshipRequest.objects.filter(to_user=user).select_related('from_user', 'to_user')
        requests = list(qs)
        return requests
        
    def sent_requests(self, user):
        """Return a list of friendship requests sent by user"""
        qs = FriendshipRequest.objects.filter(from_user=user).select_related('from_user', 'to_user')
        requests = list(qs)
        return requests
    
    def unaccepted_requests(self, user):
        """Return a list of requests that haven't been accepted"""
        qs = FriendshipRequest.objects.filter(
            to_user=user,
            rejected_at__isnull=True
        ).select_related(
            'from_user',
            'to_user'
        )
        requests = list(qs)
        return requests

    def rejected_requests(self, user):
        """Return a list of user rejected friendship requests"""
        qs = FriendshipRequest.objects.filter(
            to_user=user,
            rejected_at__isnull=False,
        ).select_related(
            'from_user',
            'to_user'
        )
        requests = list(qs)
        return requests

    def add_friend(self, from_user, to_user, message=''):
        """Create a friendship request"""
        if from_user == to_user:
            raise ValidationError('Нельзя добавить в друзья самого себя')
        
        if FriendshipRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise ValidationError('Заявка уже создана')
        
        if FriendshipRequest.objects.filter(from_user=to_user, to_user=from_user):
            raise ValidationError('Пользователь уже отправил заявку вам')
        
        if self.are_friends(from_user, to_user):
            raise ValidationError('Пользователь уже добавлен в друзья')
        
        request = FriendshipRequest.objects.create(
            from_user=from_user,
            to_user=to_user,
            message=message
        )
        request.save()
        return request

    def remove_friend(self, from_user, to_user):
        """Remove friend"""
        try:
            friend = Friend.objects.filter(
                from_user__in=[from_user, to_user],
                to_user__in=[from_user, to_user]
            )

            if friend:
                friend.delete()
                return True
            return False
        
        except Friend.DoesNotExist:
            return False
        
    def are_friends(self, user1, user2):
        if Friend.objects.filter(
                from_user__in=[user1, user2], 
                to_user__in=[user1, user2]
            ).exists():
            return True
        return False


class Friend(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friends', 
        verbose_name='От пользователя'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='_friends',
        verbose_name='К пользователю'
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    objects = FriendshipManager()

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'
        unique_together = ('from_user', 'to_user')
    
    def __str__(self) -> str:
        return f'{self.from_user} друг {self.to_user}'
    
    def save(self, *args, **kwargs) -> None:
        if self.from_user == self.to_user:
            raise ValidationError('Нельзя добавить в друзья самого себя')
        return super().save(*args, **kwargs)

class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friendship_requests_sent',
        verbose_name='От пользователя'
    )
    to_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='friendship_requests_recived',
        verbose_name='К пользователю'
    )
    message = models.TextField(blank=True, verbose_name='Сообщение')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    rejected_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата отклонения')

    class Meta:
        verbose_name = 'Заявка в друзья'
        verbose_name_plural = 'Заявки в друзья'
        unique_together = ('from_user', 'to_user')

    def __str__(self) -> str:
        return f'Заявка в друзья от {self.from_user} к {self.to_user}'
    
    def accept(self):
        """Accept friendship request"""
        Friend.objects.create(from_user=self.from_user, to_user=self.to_user)
        Friend.objects.create(from_user=self.to_user, to_user=self.from_user)

        #Delete request
        self.delete()

        #Delete cross request
        FriendshipRequest.objects.filter(from_user=self.to_user, to_user=self.from_user).delete()
        return True
    
    def reject(self):
        """Reject friendship request"""
        self.rejected_at = timezone.now()
        self.save()
        return True
    
class BlockManager(models.Manager):
    """Block manager"""

    def block(self, from_user, to_user):
        if from_user == to_user:
            raise ValidationError('Нельзя заблокировать самого себя')
        
        if self.is_blocked(from_user, to_user):
            raise ValidationError('Пользователь уже заблокирован')
        
        block = Block.objects.create(from_user=from_user, to_user=to_user)
        block.save()
        return block
    
    def unblock(self, from_user, to_user):
        try:
            block = Block.objects.filter(from_user=from_user, to_user=to_user)
            if block:
                block.delete()
                return True
            else:
                return False
            
        except Block.DoesNotExist:
            return False
    
    def blocked_users(self, user):
        qs = Block.objects.filter(from_user=user).select_related('to_user')
        blocked_users = list(qs)
        return blocked_users
    
    def is_blocked(self, user1, user2):
        if Block.objects.filter(from_user__in=[user1, user2], to_user__in=[user1, user2]).exists():
            return True
        return False

class Block(models.Model):
    from_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='black_list',
        verbose_name='Заблокировавший'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='in_black_list',
        verbose_name='Заблокированный'
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата добавления')

    objects = BlockManager()

    class Meta:
        verbose_name = 'Заблокированный пользователь'
        verbose_name_plural = 'Заблокированные пользователи'
        unique_together = ('from_user', 'to_user')

    def __str__(self) -> str:
        return f'{self.from_user} заблокировал {self.to_user}'
    
    def save(self, *args, **kwargs) -> None:
        if self.from_user == self.to_user:
            raise ValidationError('Пользователь не может заблокировать сам себя')
        return super().save(*args, **kwargs)