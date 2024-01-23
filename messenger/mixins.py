from typing import Any
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.http.response import HttpResponse


class RoomParticipantRequiredMixin:
    """Checks if user is room participant"""

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        room = self.get_object()
        if not room.participants.filter(id=request.user.id).exists():
            raise PermissionDenied("You must be a room participant")
        return super().dispatch(request, *args, **kwargs)


class RoomAdminRequiredMixin:
    """Checks if user is room admin"""

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        room = self.get_object()
        if not request.user.id == room.admin.id:
            raise PermissionDenied("You must be a room admin")
        return super().dispatch(request, *args, **kwargs)
