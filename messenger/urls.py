from django.urls import path
from . import views


app_name = "messenger"

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "direct_room_list/",
        views.RoomListView.as_view(room_type="D"),
        name="direct_room_list",
    ),
    path(
        "direct/<str:room_name>/",
        views.DirectRoomDetailView.as_view(),
        name="direct_room",
    ),
    path(
        "group_room_list/",
        views.RoomListView.as_view(room_type="G"),
        name="group_room_list",
    ),
    path("group/create/", views.GroupRoomCreateView.as_view(), name="group_create"),
    path(
        "group/<slug:room_name>/update/",
        views.GroupRoomUpdateView.as_view(),
        name="group_update",
    ),
    path(
        "group/<slug:room_name>/delete/",
        views.GroupRoomDeleteView.as_view(),
        name="group_delete",
    ),
    path(
        "group/<str:room_name>/", views.GroupRoomDetailView.as_view(), name="group_room"
    ),
]
