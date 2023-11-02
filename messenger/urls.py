from django.urls import path
from . import views

app_name = "messenger"

urlpatterns = [
    path("", views.index, name="index"),
    path("room_list/", views.GroupRoomListView.as_view(), name="room_list"),
    path(
        "direct/<str:username>/",
        views.DirectRoomDetailView.as_view(),
        name="direct_room",
    ),
    path("group/create/", views.GroupRoomCreateView.as_view(), name="group_create"),
    path(
        "group/<int:id>/update/",
        views.GroupRoomUpdateView.as_view(),
        name="group_update",
    ),
    path(
        "group/<int:id>/delete/",
        views.GroupRoomDeleteView.as_view(),
        name="group_delete",
    ),
    path(
        "group/<str:room_name>/", views.GroupRoomDetailView.as_view(), name="group_room"
    ),
]
