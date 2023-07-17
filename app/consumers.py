from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json
from asgiref.sync import async_to_sync ## এর মাধ্যমে async এর সকল Proparty কে sync এ ব্যবহার করার যায়

## NOTE Channel Layer -> দুটি বা multiple Instance নিজেদের মধ্যে জাতে Communicate করতে পারে তার জন্যে Channel Layer ব্যবহার করা হয়।

class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("Connect...........")

        print("Channel Layer = ", self.channel_layer)  
        print("Channel Name = ", self.channel_name)
        print("Consumer Group Name = ", self.scope['url_route']['kwargs']['group_name'])  


        self.groupName = self.scope['url_route']['kwargs']['group_name']  # Consumers এ self.request এর পরিবর্তে self.scope


        ## NOTE Add a channel to a new or existing group
        async_to_sync(self.channel_layer.group_add)(
            # 'Bangladesh',   # Group Name
            self.groupName,   # Group Name
            self.channel_name
        )

        self.send({
            "type": "websocket.accept",
        })




    def websocket_receive(self, event):
        print("Receive...........")
        print("------------------------------------")
        print("Channel Layer = ", self.channel_layer)  
        print("Channel Name = ", self.channel_name)
        print("Message is: ", event)
        print("Message is: ", event['text'])
        print("------------------------------------")

        async_to_sync(self.channel_layer.group_send)(
            self.groupName,{
                'type': 'chat.message',   # Chat Message Hendler টি নিচে Creat করা হয়েছে
                'message': event['text'],
            }
        )

    ## Chat Message Event Hendler টি Create করার জন্যে . এর যায় গায় শুধু _ দিতে হবে chat.message কে chat_message লিখতে হবে।
    def chat_message(self, event):
        print("------------------------------------")    
        print('Event....', event)
        print('Data', event['message']) # Data type is string 

        # এখন আমাদের এই data টি কে Text area তে দেখাতে চাইলে তা Send করতে হবে
        self.send({
            "type": "websocket.send",
            'text': event['message'],
        })
        print("------------------------------------")





    def websocket_disconnect(self, event):
        print("Disconnect...........")

        print("Channel Layer = ", self.channel_layer)  
        print("Channel Name = ", self.channel_name)

        ## NOTE Add a channel to a new or existing group
        async_to_sync(self.channel_layer.group_discard)(
            self.groupName,   # Group Name
            self.channel_name
        )
        raise StopConsumer()













class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("Connect...........")
        print("Channel Layer = ", self.channel_layer)  
        print("Channel Name = ", self.channel_name)
        print("Consumer Group Name = ", self.scope['url_route']['kwargs']['group_name'])  


        self.groupName = self.scope['url_route']['kwargs']['group_name']  # Consumers এ self.request এর পরিবর্তে self.scope


        ## NOTE Add a channel to a new or existing group
        await self.channel_layer.group_add(
            # 'Bangladesh',   # Group Name
            self.groupName,   # Group Name
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept",
        })



    async def websocket_receive(self, event):
        print("Receive...........")
        print("------------------------------------")
        print("Channel Layer = ", self.channel_layer)  
        print("Channel Name = ", self.channel_name)
        print("Message is: ", event)
        print("Message is: ", event['text'])
        print("------------------------------------")

        await self.channel_layer.group_send(
            self.groupName,{
                'type': 'chat.message',   # Chat Message Hendler টি নিচে Creat করা হয়েছে
                'message': event['text'],
            }
        )

    ## Chat Message Event Hendler টি Create করার জন্যে . এর যায় গায় শুধু _ দিতে হবে chat.message কে chat_message লিখতে হবে।
    async def chat_message(self, event):
        print("------------------------------------")    
        print('Event....', event)
        print('Data', event['message']) # Data type is string 

        # এখন আমাদের এই data টি কে Text area তে দেখাতে চাইলে তা Send করতে হবে
        await self.send({
            "type": "websocket.send",
            'text': event['message'],
        })
        print("------------------------------------")





    async def websocket_disconnect(self, event):
        print("Disconnect...........")
        print("Channel Layer = ", self.channel_layer)  
        print("Channel Name = ", self.channel_name)

        ## NOTE Add a channel to a new or existing group
        await self.channel_layer.group_discard(
            self.groupName,   # Group Name
            self.channel_name
        )
        raise StopConsumer()