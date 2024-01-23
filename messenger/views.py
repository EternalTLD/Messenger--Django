from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import QuerySet

from .models import Room
from .forms import GroupRoomCreateForm
from .mixins import RoomAdminRequiredMixin, RoomParticipantRequiredMixin


@login_required
def index(request):
    return redirect("profiles:profile_detail", username=request.user.username)


class RoomListView(LoginRequiredMixin, generic.ListView):
    """Room list view"""

    template_name = "messenger/room_list.html"
    context_object_name = "room_list"
    model = Room
    room_type = None

    def get_queryset(self) -> QuerySet[Room]:
        user = self.request.user
        room_list = self.model.objects.filter(
            participants__in=[user.id], room_type=self.room_type
        )
        return room_list


class RoomDetailView(RoomParticipantRequiredMixin, generic.DetailView):
    """Base room detail view"""

    template_name = "messenger/room.html"
    model = Room
    slug_field = "name"
    slug_url_kwarg = "room_name"


class DirectRoomDetailView(RoomDetailView):
    """Direct room detail view"""

    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        room = get_object_or_404(
            self.model, name=self.kwargs.get("room_name"), room_type="D"
        )
        room_title = room.participants.exclude(id=request.user.id).first()
        return render(
            request, self.template_name, {"room": room, "room_title": room_title}
        )


class GroupRoomDetailView(RoomDetailView):
    """Group room detail view"""

    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        room = get_object_or_404(
            self.model, name=self.kwargs.get("room_name"), room_type="G"
        )
        return render(
            request, self.template_name, {"room": room, "room_title": room.name}
        )


class GroupRoomCreateView(LoginRequiredMixin, generic.CreateView):
    model = Room
    form_class = GroupRoomCreateForm
    template_name = "messenger/create_group_room.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        room = form.save(commit=False)
        room.admin = self.request.user
        room.room_type = "G"
        room.save()
        form.save_m2m()
        room.participants.add(self.request.user)
        return redirect("messenger:group_room", room_name=room.name)

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class GroupRoomUpdateView(RoomAdminRequiredMixin, generic.UpdateView):
    model = Room
    form_class = GroupRoomCreateForm
    template_name = "messenger/update_group_room.html"
    slug_field = "name"
    slug_url_kwarg = "room_name"

    def get_success_url(self) -> str:
        return redirect("messenger:group_room", room_name=self.kwargs.pop("room_name"))

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class GroupRoomDeleteView(RoomAdminRequiredMixin, generic.DeleteView):
    model = Room
    template_name = "messenger/room_delete.html"
    success_url = reverse_lazy("messenger:room_list")
    slug_field = "name"
    slug_url_kwarg = "room_name"
