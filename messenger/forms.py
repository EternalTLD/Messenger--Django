from django import forms

from .models import Room


class GroupRoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "participants"]
