import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from channels.consumer import SyncConsumer, AsyncConsumer
from django.contrib.auth.models import AnonymousUser

from . import tasks

# COMMANDS = {
#     'help': {
#         'help': 'Display help message.',
#     },
#     'sum': {
#         'args': 2,
#         'help': 'Calculate sum of two integer arguments. Example: `sum 12 32`.',
#         'task': 'add'
#     },
#     'status': {
#         'args': 1,
#         'help': 'Check website status. Example: `status twitter.com`.',
#         'task': 'url_status'
#     },
# }

# class ChatConsumer(WebsocketConsumer):
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         response_message = 'Please type `help` for the list of the commands.'
#         message_parts = message.split()
#         if message_parts:
#             command = message_parts[0].lower()
#             if command == 'help':
#                 response_message = 'List of the available commands:\n' + '\n'.join([f'{command} - {params["help"]} ' for command, params in COMMANDS.items()])
#             elif command in COMMANDS:
#                 if len(message_parts[1:]) != COMMANDS[command]['args']:
#                     response_message = f'Wrong arguments for the command `{command}`.'
#                 else:
#                     getattr(tasks, COMMANDS[command]['task']).delay(self.channel_name, *message_parts[1:])
#                     response_message = f'Command `{command}` received.'
        
#         async_to_sync(self.channel_layer.send)(
#                 self.channel_name,
#                 {
#                     'type': 'chat_message',
#                     'message': response_message
#                 }
#             )

#     def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': f'[bot]: {message}'
#         }))


users = {}

class CoordConsumer(JsonWebsocketConsumer):
    # https://stackoverflow.com/questions/57751915/django-channels-jsonwebsocketconsumer-self-send-json-error
    # https://channels.readthedocs.io/en/latest/topics/consumers.html
    # https://channels.readthedocs.io/en/latest/topics/channel_layers.html#groups
    # https://stackoverflow.com/questions/51931038/django-how-to-track-if-a-user-is-online-offline-in-realtime
    # https://github.com/uuidjs/uuid

    groups = ["broadcast"]
    uuid=""

    def receive_json(self, content):
        """
        Will receive "{x:float, y:float, z:float, uuid:uuid4}"
        text_data_json = json.loads(text_data)
        as per ASGI's at-most-once delivery policy, don't send if unchanged
        
        {
            uuid: str,
            x,
            y
        }
        """

        # if we haven't set a UUID for this connection:
        if self.uuid=="":
            self.uuid = content["uuid"]

        # if the values for this UUID are different, update the shit.
        if users.get(content["uuid"]) != content:
            users[content["uuid"]] = content

            # send to the group, which will include everybody who is connected to the app.
            # group_send is an async method, but JsonWebSocketConsumer is sync as we may put database stuff in it later
            # So first convert group_send to sync
            # then give it the groupname
            # type: the fn to call within this consumer
            # content: content to feed the fn
            async_to_sync(self.channel_layer.group_send)("broadcast", {
                "type":"broadcast_coordinates",
                "users":users
            })


    def disconnect(self, close_code):
        # remove the uuid from the list of users
        users.pop(self.uuid, None)


    def broadcast_coordinates(self, event):
        # send_json
        self.send_json(event["users"])


# {'type': 'websocket', 
# 'path': '/ws/gallery/', 
# 'raw_path': b'/ws/gallery/', 
# 'headers': [
#     (b'host', b'127.0.0.1:8000'), 
#     (b'user-agent', b'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0'),
#     (b'accept', b'*/*'), 
#     (b'accept-language', b'en-US,en;q=0.5'), 
#     (b'accept-encoding', b'gzip, deflate'), 
#     (b'sec-websocket-version', b'13'), 
#     (b'origin', b'http://127.0.0.1:8000'), 
#     (b'sec-websocket-extensions', b'permessage-deflate'), 
#     (b'sec-websocket-key', b't+kN4RItNV2XqQD10wa9yA=='), 
#     (b'dnt', b'1'), 
#     (b'connection', b'keep-alive, Upgrade'), 
#     (b'pragma', b'no-cache'), 
#     (b'cache-control', b'no-cache'), 
#     (b'upgrade', b'websocket')
# ],
# 'query_string': b'', 
# 'client': ['127.0.0.1', 38552], 
# 'server': ['127.0.0.1', 8000], 
# 'subprotocols': [], 
# 'path_remaining': '', 
# 'url_route': {'args': (), 'kwargs': {}}}