from email import message
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.core.cache import cache
import random


def message_for_send_list_user(self, listUser):
    messageTest = ""
    for user in listUser:
        messageTest += user + str(";")

    message = messageTest[:-1]

    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'list_user',
            'message': message
        }
    )


class GameConsumer(WebsocketConsumer):
    index = -1
    is_guest = -1

    def connect(self):
        self.index = len(self.scope['session']['joined_game'])
        self.room_group_name = self.scope['session']['joined_game'][self.index - 1]  # ID Game
        listUser = cache.get(self.scope['session']['joined_game'][self.index - 1] + "_users", list())
        list_users_score = cache.get(self.scope['session']['joined_game'][self.index - 1] + "_users_scores", list())


        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.is_guest = 1
        if (len(listUser) == 0):
            self.is_guest = 0

        self.accept()
        listUser.append(self.scope['session']['name'] + str(self.is_guest))
        list_users_score.append((self.scope['session']['name'], self.scope['session']['player_id'], 0))
        cache.set(self.scope['session']['joined_game'][self.index - 1] + "_users", listUser, 7200)
        cache.set(self.scope['session']['joined_game'][self.index - 1] + "_users_scores", list_users_score, 7200)
        message_for_send_list_user(self, listUser)

    def receive(self, text_data):
        data_json = json.loads(text_data)
        redirect = data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'redirect',
                'message': 'startgame'
            }
        )

        self.send(text_data=json.dumps({
            'type': 'response',
            'message': 'tableau'
        }))

    def redirect(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'redirection',
            'message': message
        }))

    def user_check(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'response',
            'message': message
        }))

    def list_user(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'users',
            'message': message
        }))

    def disconnect(self, code):
        listUser = cache.get(self.scope['session']['joined_game'][self.index - 1] + "_users")

        listUser.remove(self.scope['session']['name'] + str(self.is_guest))

        cache.set(self.scope['session']['joined_game'][self.index - 1] + "_users", listUser, 7200)

        message_for_send_list_user(self, listUser)
