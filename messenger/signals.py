from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from friends.models import Friend
from .models import Room


@receiver(post_save, sender=Friend)
def create_direct_chat_room(sender, instance, **kwargs):
    """Create a chat room when users become friends"""
    first_user = instance.from_user.username
    second_user = instance.to_user.username
    room = Room.objects.create(name=f"{first_user}_{second_user}", room_type="D")
    room.participants.add(first_user, second_user)

    # Delete cross room
    if Room.objects.filter(name=f"{second_user}_{first_user}", room_type="D").exists():
        Room.objects.get(name=f"{second_user}_{first_user}", room_type="D").delete()


@receiver(post_delete, sender=Friend)
def delete_direct_chat_room(sender, instance, **kwargs):
    """Delete a chat room when users stop being friends"""
    first_user = instance.from_user.username
    second_user = instance.to_user.username

    if Room.objects.filter(name=f"{first_user}_{second_user}", room_type="D").exists():
        Room.objects.get(name=f"{first_user}_{second_user}", room_type="D").delete()

    if Room.objects.filter(name=f"{second_user}_{first_user}", room_type="D").exists():
        Room.objects.get(name=f"{second_user}_{first_user}", room_type="D").delete()
