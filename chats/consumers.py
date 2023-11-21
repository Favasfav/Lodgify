# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer

# class ChatConsumer(WebsocketConsumer):
#     def connect(self,*args,**kwargs):
#         current_user=int(self.scope["query_string"])
#         other_user_id=self.scop["url_route"]["kwargs"]["id"]

#         self.room_name = f"{current_user}_{other_user_id}"
#         self.room_group_name = f"chat_{self.room_name}"

#         # Join room group
#         self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         self.accept()


#     def disconnect(self, close_code):
#        # Leave room group
#         self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )



#     def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']

#         # Save the message to the database
#         sender_username = data['sender']
#         receiver_username = data['receiver']

        
#         # receiver = CustomUser.objects.get(username=receiver_username)
#         # Chat.objects.create(sender=sender, receiver=receiver, message=message)

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': sender_username,
#             }
#         )



#     async def chat_message(self, event):
#         message = event['message']
#         sender = event['sender']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'sender': sender,
#         }))


import json,os
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .serializers import *
from accounts.models import *
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
class ChatConsumer(AsyncWebsocketConsumer):
    print('------------------...,,,,..')
    async def connect(self):
        print('ldkfnsldfknsd;ofnsd;fonds;fn;f')
        # current_user = self.scope["query_string"]
        current_user = int(self.scope["query_string"])
        other_user_id = self.scope["url_route"]["kwargs"]["user_id"]
       
        print(current_user,other_user_id,'------------------...,,,,..')

        # current_user = int(self.scope["query_string"].decode("utf-8"))
        # other_user_id = self.scope["url_route"]["kwargs"]["id"]
        self.room_name = (
            f"{current_user}_{other_user_id}"
            if int(current_user) > int(other_user_id)
            else f"{other_user_id}_{current_user}"
        )
     
        self.room_group_name = f"chat_{self.room_name}"
        print("-----------------",self.room_group_name,"--------room",self.channel_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print('connected--->')

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await super().disconnect(close_code)

    async def receive(self, text_data=None,bytes_data=None):
        data = json.loads(text_data)
        print(data,"data-----------")
        message = data['message']
        sender_id = data['sender']
        # Save the message to the database
        receiver_id = data['receiver']
        
        reciever_obj=  PartnerProfile.objects.get(id=receiver_id)
        print("reciever-=-----============",reciever_obj)
        print(reciever_obj.user)
        receiver  = reciever_obj.user
        print("reciever-=-----=hhhhh===========",receiver)
        sender = await self.get_user(sender_id)
        print("dender",sender)
       
        print("senderrecirve-00000000",sender,receiver)
        await self.save_message(
            sender=sender, reciever=receiver, message=message, thread_name=self.room_group_name
        )

        messages = await self.get_messages()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender_id,
                "messages": messages,
            },
        )




    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        messages=event['messages']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'messages':messages
        }))

        # async def chat_message(self, event):
        #     message = event["message"]
        #     username = event["senderUsername"]
        #     messages = event["messages"]

        #     await self.send(
        #         text_data=json.dumps(
        #             {
        #                 "message": message,
        #                 "senderUsername": username,
        #                 "messages": messages,
        #             }
        #         )
        #     )

    @database_sync_to_async
    def get_user(self, id):
        return CustomUser.objects.get(id=id)



    @database_sync_to_async
    def get_messages(self):
        from .serializers import MessageSerializer
        from .models import Message
        messages = []
        for instance in Message.objects.filter(thread_name=self.room_group_name):
            messages = MessageSerializer(instance).data
        return messages

    @database_sync_to_async
    def save_message(self, sender, reciever, message, thread_name):
        from .serializers import MessageSerializer
        from .models import Message
        Message.objects.create(
            sender=sender, receiver=reciever, message=message, thread_name=thread_name
        )
