import json
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Q
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Message, Room


User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.messages_to_paginate = 10

    def get_start_messages(self):
        try:
            self.last_uploaded_message_id = Message.objects.filter(room=self.room).first().id
            self.first_uploaded_message_id = Message.objects.filter(room=self.room)[
                self.messages_to_paginate - 1
            ].id
        except AttributeError:
            self.last_uploaded_message_id = None
            self.first_uploaded_message_id = None
        except IndexError:
            self.first_uploaded_message_id = Message.objects.filter(room=self.room).last().id

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.room = Room.objects.get(name=self.room_name)
        self.user = self.scope["user"]
        self.get_start_messages()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json["type"] == "chat_message":
            content = text_data_json["content"]
            new_message = self.save_message(content)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": {
                        "author": self.user.username,
                        "content": new_message.content,
                        "timestamp": datetime.strftime(
                            new_message.timestamp, "%Y-%m-%d %H:%M"
                        ),
                    },
                },
            )

        if text_data_json["type"] == "paginate":
            messages = self.get_room_messages()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "paginate", "message": messages}
            )

        if text_data_json["type"] == "fetch_messages":
            messages = self.get_room_messages()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "fetch_messages", "message": messages}
            )

    def save_message(self, content):
        message = Message.objects.create(
            author=self.user, content=content, room=self.room
        )
        return message

    def get_room_messages(self):
        if self.first_uploaded_message_id and self.last_uploaded_message_id:
            messages = Message.objects.filter(
                Q(id__gte=self.first_uploaded_message_id),
                Q(id__lte=self.last_uploaded_message_id),
                room = self.room
            )
            messages = [
                {
                    "author": message.author.username,
                    "content": message.content,
                    "timestamp": datetime.strftime(message.timestamp, "%Y-%m-%d %H:%M"),
                }
                for message in messages
            ]

            self.first_uploaded_message_id -= self.messages_to_paginate
            self.last_uploaded_message_id -= self.messages_to_paginate

            return messages
        return None

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def fetch_messages(self, event):
        self.send(text_data=json.dumps(event))

    def paginate(self, event):
        self.send(text_data=json.dumps(event))
