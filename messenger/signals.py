from django.db.models.signals import post_save
from django.dispatch import receiver

from friends.models import Friend
from .models import Room

@receiver(post_save, sender=Friend)
def create_direct_chat_room(sender, instance, created, **kwargs):
    if created:
        first_user = instance.from_user
        second_user = instance.to_user
        room = Room.objects.create(
            name=f'{first_user.username}_{second_user.username}'
        )
        room.participants.add(first_user, second_user)

        try:
            cross_room = Room.objects.get(name=f'{second_user.username}_{first_user.username}')
            cross_room.delete()
        except Room.DoesNotExist:
            print('ok')