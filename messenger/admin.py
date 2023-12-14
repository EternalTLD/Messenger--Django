from django.contrib import admin

from .models import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "admin", "room_type", "members_count")
    search_fields = ("name",)
    list_filter = ("room_type",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("author", "short_content", "timestamp", "room")
    search_fields = ("author", "content")
    list_filter = ("timestamp",)

    @admin.display(description="Content")
    def short_content(self, obj):
        return (obj.content[:30] + "...") if len(obj.content) > 30 else obj.content
