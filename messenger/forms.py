from typing import Any
from django import forms
from django.contrib.auth import get_user_model

from .models import Room


class GroupRoomCreateForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ["name", "participants"]

    def __init__(self, user, *args: Any, **kwargs: Any) -> None:
        super(GroupRoomCreateForm, self).__init__(*args, **kwargs)
        self.fields['participants'].queryset = get_user_model().objects.filter(
            id__in=user.friends.values_list("to_user", flat=True)
        )
