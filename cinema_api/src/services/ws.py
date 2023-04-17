from typing import Dict, List

from fastapi.encoders import jsonable_encoder
from models.room import RoomUserMessage, RoomUserMessageTypeEnum
from services.room import RoomService
from starlette.websockets import WebSocket


class WebsocketService(RoomService):
    def __init__(self, *args, **kwargs):
        self.active_connections: List[WebSocket] = []
        super().__init__(*args, **kwargs)

    async def connect(self, room_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.stream_message(
            room_id=room_id,
            websocket=websocket,
            message=f"{websocket.user.first_name} {websocket.user.last_name} присоединился к комнате!",
            message_type=RoomUserMessageTypeEnum.service.value,
        )

    async def disconnect(self, room_id: str, websocket: WebSocket) -> None:
        await self.stream_message(
            room_id=room_id,
            websocket=websocket,
            message=f"{websocket.user.first_name} {websocket.user.last_name} покинул комнату!",
            message_type=RoomUserMessageTypeEnum.service.value,
        )
        self.active_connections.remove(websocket)

    async def read_from_stream(self, room_id: str, websocket: WebSocket) -> None:
        resp = await self.redis.xread({room_id: "$"}, None, 0)
        _, messages = resp[0]
        for message in messages:
            msg = jsonable_encoder(message[1])
            await websocket.send_json(msg)

    async def _send_msg(self, room_id: str, message: Dict):
        await self.redis.xadd(room_id, fields=message)

    async def stream_message(
        self,
        room_id: str,
        message: str,
        websocket: WebSocket,
        message_type: RoomUserMessageTypeEnum = RoomUserMessageTypeEnum.user.value,
    ):
        prepared_message = jsonable_encoder(
            RoomUserMessage(
                text=message,
                msg_type=message_type,
                user_id=websocket.user.pk,
                first_name=websocket.user.first_name,
                last_name=websocket.user.last_name,
            ).dict()
        )
        await self._send_msg(room_id, prepared_message)
