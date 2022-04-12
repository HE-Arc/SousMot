import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test' #ID Game
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        
        # Test connection
        # self.send(text_data=json.dumps({
        #     'type' : 'connection_established',
        #     'message' : 'You are now connected!'
        # }))
    
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