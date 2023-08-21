from django.contrib import admin

from .models import Friend, FriendshipRequest, Block


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    raw_id_fields = ("to_user", "from_user")

@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin):
    raw_id_fields = ("from_user", "to_user")

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    raw_id_fields = ("from_user", "to_user")