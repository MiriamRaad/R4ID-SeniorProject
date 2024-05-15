from django.shortcuts import render
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
import asyncio,json


#Location Streaming Websocket Connection
class locationstreaming(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.loop = asyncio.get_event_loop()
        self.groupname = "Locationstreaming"

    async def connect(self):
        # Initialization code when a WebSocket connection is established
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
        )
        print(self.groupname)
        print(self.channel_name)
        await self.accept()
        print("WebSocket Location streaming connection established")

    async def disconnect(self, close_code):
        print("WebSocket Location streaming connection disconnected")
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
        raise StopConsumer()

    async def receive(self,text_data):

            self.json_coordinates = json.loads(text_data)
            self.lat = self.json_coordinates['lat']
            self.lon = self.json_coordinates['long']

            print(self.json_coordinates['lat'])

            # Broadcast the base64-encoded image to all connected clients
            await self.channel_layer.group_send(
                self.groupname,
                {
                    'type': 'send_location',
                     'lat':  self.lat,
                     'lon': self.lon,
                }
            )

    async def send_location(self, event):
        lat = event['lat']
        long = event['lon']
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps(
            {
                'lat':lat,
                "long":long,
            }))


def locationstreamingrender(request):
    return render(request, 'GPSTracking.html')
