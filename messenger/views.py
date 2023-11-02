from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Room, Message
from .forms import GroupRoomCreateForm


User = get_user_model()


def index(request):
    return render(request, "messenger/index.html", {"title": "Welcome"})


class GroupRoomListView(ListView):
    template_name = "messenger/room_list.html"
    context_object_name = "room_list"

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        room_list = Room.objects.filter(
            Q(participants__in=[user.id]) | Q(admin=user), room_type="G"
        ).distinct()
        return room_list


class DirectRoomDetailView(DetailView):
    template_name = "messenger/room.html"

    def get(self, request, *args, **kwargs):
        first_user = request.user
        second_user = get_object_or_404(User, username=self.kwargs.get("username"))

        if Room.objects.filter(
            name=f"{first_user.username}_{second_user.username}", room_type="D"
        ).exists():
            room = Room.objects.get(
                name=f"{first_user.username}_{second_user.username}", room_type="D"
            )
        elif Room.objects.filter(
            name=f"{second_user.username}_{first_user.username}", room_type="D"
        ).exists():
            room = Room.objects.get(
                name=f"{second_user.username}_{first_user.username}", room_type="D"
            )
        else:
            raise ObjectDoesNotExist("Room does not exist")

        return render(
            request, "messenger/room.html", {"room": room, "to_user": second_user}
        )


class GroupRoomCreateView(CreateView):
    model = Room
    fields = ["name", "participants"]
    template_name = "messenger/create_group_room.html"
    success_url = reverse_lazy("messenger:room_list")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        room = form.save(commit=False)
        room.admin = self.request.user
        room.save()
        return super().form_valid(form)


class GroupRoomUpdateView(UpdateView):
    model = Room
    fields = ["name", "participants"]
    template_name = "messenger/update_group_room.html"


class GroupRoomDeleteView(DeleteView):
    model = Room
    success_url = reverse_lazy("messenger:room_list")


class GroupRoomDetailView(DetailView):
    template_name = "messenger/group_room.html"

    def get(self, request, *args, **kwargs):
        room = get_object_or_404(Room, name=self.kwargs.get("room_name"), room_type="G")

        return render(
            request, "messenger/room.html", {"room": room, "to_user": room.name}
        )
