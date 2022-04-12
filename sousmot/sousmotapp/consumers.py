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
                'type' : 'list_user',
                'message' : message
            }
        )

class GameConsumer(WebsocketConsumer):
    
    def connect(self):
        self.room_group_name = 'test' #ID Game
        listUser = cache.get("test_users", list())
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        listUser.append(self.scope['session']['name'])
        cache.set("test_users", listUser, 7200) 
        message_for_send_list_user(self, listUser)
        
    
        
    
    def receive(self, text_data):
        data_json = json.loads(text_data)
        word = data_json['message']
        
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'user_check',
                'message' : 'One player check his word'
            }
        )
        
        self.send(text_data=json.dumps({
            'type' : 'response',
            'message' : 'tableau'
        }))
    
    def user_check(self, event):
        message = event['message']
        
        self.send(text_data=json.dumps({
            'type' : 'response',
            'message' : message
        }))
    
    def list_user(self, event):
        message = event['message']
        
        self.send(text_data=json.dumps({
            'type' : 'users',
            'message' : message
        }))
    
    def disconnect(self, code):
        listUser = cache.get("test_users")
        
        listUser.remove(self.scope["user"])
        
        cache.set("test_users", listUser, 7200)  
        message_for_send_list_user(self, listUser)
        
    