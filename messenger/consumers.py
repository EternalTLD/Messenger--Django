import json
from datetime import datetime

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Message, Room


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.messages_to_paginate = settings.MESSAGES_TO_PAGINATE

    def get_messages(self, page):
        queryset = Message.objects.filter(room=self.room)
        paginator = Paginator(queryset, self.messages_to_paginate)

        try:
            messages_page = paginator.page(page)
        except EmptyPage:
            return None
        
        messages = [
            {
            "author": message.author.username,
            "content": message.content,
            "timestamp": datetime.strftime(message.timestamp, "%Y-%m-%d %H:%M"),
            } for message in messages_page.object_list[::-1]
        ]
        return messages


    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.room = Room.objects.get(name=self.room_name)
        self.user = self.scope["user"]

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
        command = text_data_json.get("type")

        if command == "chat_message":
            content = text_data_json.get("content")
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

        if command == "fetch_messages":
            messages = self.get_messages(text_data_json.get("page"))

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "fetch_messages", "message": messages}
            )

    def save_message(self, content):
        message = Message.objects.create(
            author=self.user, content=content, room=self.room
        )
        return message

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def fetch_messages(self, event):
        self.send(text_data=json.dumps(event))

    def paginate(self, event):
        self.send(text_data=json.dumps(event))
