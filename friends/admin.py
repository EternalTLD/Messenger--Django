from django.contrib import admin

from .models import Friend, FriendshipRequest


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ("to_user", "from_user", "friends_since")
    search_fields = ("to_user__username", "from_user__username")
    list_filter = ("created_at", )
    actions = ["remove_friend"]

    def friends_since(self, obj):
        return obj.created_at.strftime("%d/%m/%Y")
    
    @admin.action(description="Remove selected friends")
    def remove_friend(self, request, queryset):
        for friend in queryset:
            friend.delete()
    

@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user", "status", "created_at", "rejected_at")
    search_fields = ("to_user__username", "from_user__username")
    list_filter = ("created_at", "rejected_at")
    actions = ["accept_request", "reject_request"]

    def status(self, obj):
        if obj.rejected_at:
            return "Rejected"
        return "Pending"
    
    @admin.action(description='Accept selected friendship requests')
    def accept_request(self, request, queryset):
        for fr in queryset:
            fr.accept()
    
    @admin.action(description='Reject selected friendship requests')
    def reject_request(self, request, queryset):
        for fr in queryset:
            fr.reject()
