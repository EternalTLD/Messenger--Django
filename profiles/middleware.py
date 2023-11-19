from typing import Any
from django.utils import timezone
from django.core.cache import cache

from .models import Profile


class UserActivityMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request) -> Any:
        if request.user.is_authenticated and request.session.session_key:
            cache_key = f"last_activity_{request.user.id}"
            last_activity = cache.get(cache_key)

            if not last_activity:
                Profile.objects.filter(user=request.user).update(last_seen=timezone.now())
                cache.set(cache_key, timezone.now(), 300)
        
        response = self.get_response(request)
        return response