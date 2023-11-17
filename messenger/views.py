from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Room
from .services import get_direct_room_title


@login_required
def index(request):
    return redirect("profiles:profile_detail", username=request.user.username)


class DirectRoomListView(ListView):
    template_name = "messenger/room_list.html"
    context_object_name = "room_list"

    def get_queryset(self) -> QuerySet[Room]:
        user = self.request.user
        room_list = Room.objects.filter(
            participants__in=[user.id], room_type="D"
        ).distinct()
        return room_list


class DirectRoomDetailView(DetailView):
    template_name = "messenger/room.html"

    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        room_name = self.kwargs.get("room_name")
        room = get_object_or_404(Room, name=room_name, room_type="D")
        room_title = get_direct_room_title(request.user.username, room_name)

        return render(
            request, "messenger/room.html", {"room": room, "room_title": room_title}
        )


class GroupRoomListView(ListView):
    template_name = "messenger/room_list.html"
    context_object_name = "room_list"

    def get_queryset(self) -> QuerySet[Room]:
        user = self.request.user
        room_list = Room.objects.filter(
            Q(participants__in=[user.id]) | Q(admin=user), room_type="G"
        ).distinct()
        return room_list


class GroupRoomDetailView(DetailView):
    template_name = "messenger/group_room.html"

    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        room = get_object_or_404(Room, name=self.kwargs.get("room_name"), room_type="G")

        return render(
            request, "messenger/room.html", {"room": room, "room_title": room.name}
        )


class GroupRoomCreateView(CreateView):
    model = Room
    fields = ["name", "participants"]
    template_name = "messenger/create_group_room.html"
    success_url = reverse_lazy("messenger:room_list")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        room = form.save(commit=False)
        room.admin = self.request.user
        room.room_type = "G"
        room.save()
        return super().form_valid(form)


class GroupRoomUpdateView(UpdateView):
    model = Room
    fields = ["name", "participants"]
    template_name = "messenger/update_group_room.html"


class GroupRoomDeleteView(DeleteView):
    model = Room
    success_url = reverse_lazy("messenger:room_list")
