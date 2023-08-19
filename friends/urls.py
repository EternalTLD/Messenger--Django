from django.urls import path
from friends.views import (add_friend_view, accept_request_view,
                           reject_request_view, remove_friend_view,
                           unaccepted_requests_view, friends_list_view,
                           block_user_view,unblock_user_view, blocked_users_list_view)


app_name = 'friends'

urlpatterns = [
    path('friends_list/', friends_list_view, name='friends_list'),
    path('friendship_requests/', unaccepted_requests_view, name='friendship_requests'),
    path('accept_request/<int:friendship_request_id>', accept_request_view, name='request_accept'),
    path('reject_request/<int:friendship_request_id>', reject_request_view, name='request_reject'),
    path('add_friend/<str:to_username>/', add_friend_view, name='friend_add'),
    path('remove_friend/<str:to_username/', remove_friend_view, name='friend_remove'),
    path('block/<str:to_username>/', block_user_view, name='user_block'),
    path('unblock/<str:to_username>/', unblock_user_view, name='user_unblock'),
    path('block_list/', blocked_users_list_view, name='blocked_users_list')
]