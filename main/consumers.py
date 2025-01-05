import logging
from channels.generic.websocket import AsyncWebsocketConsumer



class SimpleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data="¡Conexión exitosa al servidor WebSocket!")
        print(f"Cliente conectado: {self.channel_name}")

    async def disconnect(self, close_code):
        print(f"Cliente desconectado: {self.channel_name}")
