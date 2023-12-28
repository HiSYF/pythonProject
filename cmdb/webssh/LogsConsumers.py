import asyncio
import logging
import os

import aiofiles
from channels.generic.websocket import AsyncJsonWebsocketConsumer

logger = logging.getLogger(__name__)


class RobotMessageConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.disconnected = True

    async def connect(self):
        username = self.scope["url_route"]["kwargs"].get('username')
        token = self.scope["url_route"]["kwargs"].get('token')

        if username == token:
            self.disconnected = False
            self.room_group_name = f"message_{username}"
            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            logger.error(f"username:{username} token:{token} auth failed")
            await self.close()

    async def disconnect(self, close_code):
        self.disconnected = True
        if self.room_group_name:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive_json(self, content, **kwargs):
        filepath = content.get('filepath')
        await self.async_handle_task(filepath)

    async def async_handle_task(self, filepath):
        while not self.disconnected:
            if not os.path.exists(filepath):
                await self.send_json({'message': '.', 'filepath': filepath})
                await asyncio.sleep(0.5)
            else:
                await self.send_task_log(filepath)
                break

    async def send_task_log(self, filepath):
        await self.send_json({'message': '\r\n'})
        try:
            logger.debug('file log path: {}'.format(filepath))
            async with aiofiles.open(filepath, 'rb') as log_f:
                await log_f.seek(0, os.SEEK_END)
                print(await log_f.tell())
                backup = min(4096 * 5, await log_f.tell())
                await log_f.seek(-backup, os.SEEK_END)
                while not self.disconnected:
                    data = await log_f.read(4096)
                    if data:
                        data = data.replace(b'\n', b'\r\n')
                        await self.send_json(
                            {'message': data.decode(errors='ignore'), 'filepath': filepath}
                        )
                    await asyncio.sleep(0.2)
        except OSError as e:
            logger.warning('file log path open failed: {}'.format(e))