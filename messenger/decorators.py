from functools import wraps
from django.core.exceptions import PermissionDenied

from .models import Room


def is_room_participant(view_func):
    """Checks if user is room participant"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            Room.objects.get(participants__in=[request.user.id], name=kwargs.get("room_name"))
        except Room.DoesNotExist:
            raise PermissionDenied("You must be a room participant")
        
        return view_func(request, *args, **kwargs)
    return wrapper
        