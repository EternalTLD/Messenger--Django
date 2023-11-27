from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q, QuerySet

from .models import Room
from .forms import GroupRoomCreateForm


@login_required
def index(request):
    return redirect("profiles:profile_detail", username=request.user.username)


class DirectRoomListView(generic.ListView):
    template_name = "messenger/room_list.html"
    context_object_name = "room_list"
    model = Room

    def get_queryset(self) -> QuerySet[Room]:
        user = self.request.user
        room_list = self.model.objects.filter(
            participants__in=[user.id], room_type="D"
        ).distinct()
        return room_list


class DirectRoomDetailView(generic.DetailView):
    template_name = "messenger/room.html"

    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        room = get_object_or_404(Room, name=self.kwargs.get("room_name"), room_type="D")
        room_title = room.participants.exclude(id=request.user.id).first()
        return render(
            request, self.template_name, {"room": room, "room_title": room_title}
        )


class GroupRoomListView(generic.ListView):
    template_name = "messenger/room_list.html"
    context_object_name = "room_list"

    def get_queryset(self) -> QuerySet[Room]:
        user = self.request.user
        room_list = Room.objects.filter(
            Q(participants__in=[user.id]) | Q(admin=user), room_type="G"
        ).distinct()
        return room_list


class GroupRoomDetailView(generic.DetailView):
    template_name = "messenger/room.html"

    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        room = get_object_or_404(Room, name=self.kwargs.get("room_name"), room_type="G")
        return render(
            request, self.template_name, {"room": room, "room_title": room.name}
        )


class GroupRoomCreateView(generic.CreateView):
    model = Room
    form_class = GroupRoomCreateForm
    template_name = "messenger/create_group_room.html"
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        if form.is_valid():
            room = form.save(commit=False)
            room.admin = request.user
            room.room_type = "G"
            room.save()
            form.save_m2m()
            return redirect("messenger:group_room", room_name=room.name)
        return render(request, self.template_name, {"form": form})
    
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class GroupRoomUpdateView(generic.UpdateView):
    model = Room
    form_class = GroupRoomCreateForm
    template_name = "messenger/update_group_room.html"

    def get_success_url(self) -> str:
        return redirect("messenger:group_room", room_name=self.kwargs.pop("room_name"))


class GroupRoomDeleteView(generic.DeleteView):
    model = Room
    success_url = reverse_lazy("messenger:room_list")
