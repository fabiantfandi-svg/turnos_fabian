import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AlertaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'alertas_group'

        # Unirse al grupo de alertas
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Este método se activa cuando enviamos algo desde las Views
    async def enviar_alerta(self, event):
        mensaje = event['mensaje']

        # Enviar el mensaje al cliente (Postman o Frontend)
        await self.send(text_data=json.dumps({
            'alerta': mensaje
        }))