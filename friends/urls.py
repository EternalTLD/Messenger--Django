from django.urls import path
from friends.views import (add_friend_view, accept_friend_view,
                           reject_friend_view, remove_friend_view,
                           unaccepted_friendship_requests_view,
                           friends_list_view)


app_name = 'friends'

urlpatterns = [
    path('friends_list/', friends_list_view, name='friends_list'),
    path('friendship_requests/', unaccepted_friendship_requests_view, name='friendship_requests'),
    path('accept_friend/<int:friendship_request_id>', accept_friend_view, name='friend_accept'),
    path('reject_friend/<int:friendship_request_id>', reject_friend_view, name='friend_reject'),
    path('add_friend/<str:to_username>/', add_friend_view, name='friend_add'),
    path('remove_friend/<str:to_username/', remove_friend_view, name='friend_remove'),
]