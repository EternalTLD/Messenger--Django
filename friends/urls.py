from django.urls import path
from . import views


app_name = "friends"

urlpatterns = [
    path("friend_list/", views.friend_list_view, name="friend_list"),
    path("search_friend/", views.search_friend_view, name="friend_search"),
    path("rejected_requests/", views.rejected_requests_view, name="rejected_requests"),
    path(
        "unaccepted_requests/",
        views.unaccepted_requests_view,
        name="unaccepted_requests",
    ),
    path("add/", views.add_friend_view, name="friend_add"),
    path("remove/", views.remove_friend_view, name="friend_remove"),
    path("request/accept/", views.accept_request_view, name="request_accept"),
    path("request/reject/", views.reject_request_view, name="request_reject"),
]
