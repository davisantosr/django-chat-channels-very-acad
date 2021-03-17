import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatRoomConsumer(AsyncJsonWebsocketConsumer):
  async def connect(self):
    # get the room name from the variable
    self.room_name = self.scope['url_route']['kwargs']['room_name']

    #create a group room with the given room name
    self.room_group_name = 'chat_%s' % self.room_name

    await self.channel_layer.group_add(
      self.room_group_name, 
      self.channel_name
    )

    await self.accept()
    
    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'tester_message',
        'tester': 'testing',
      }
    )


  # function defined with the same name as type on the group_send
  async def tester_message(self, event):
    tester = event['tester']

    await self.send(text_data=json.dumps({
      'tester': tester,
    }))

  async def disconnect(self, close_code):
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )
  pass