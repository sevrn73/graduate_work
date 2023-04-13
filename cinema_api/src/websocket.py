import asyncio
from functools import lru_cache

import uvicorn
from aioredis import Redis
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncEngine

from connection_events.events import on_shutdown, on_startup
from connection_events.postgres import get_pg_engine
from connection_events.redis import get_redis_client
from core.auth.decorators import ws_room_permission
from core.auth.models import CustomUser
from core.auth.middleware import JWTBearer
from core.config import settings
from services.ws import WebsocketService


app = FastAPI(
    on_startup=on_startup,
    on_shutdown=on_shutdown,
)


@lru_cache()
def get_ws_service(
    db_connection: AsyncEngine = Depends(get_pg_engine),
    redis: Redis = Depends(get_redis_client),
) -> WebsocketService:
    return WebsocketService(db_connection, redis)


async def read_from_stream(room_id: str, service: WebsocketService, websocket: WebSocket):
    while True:
        await service.read_from_stream(room_id=room_id, websocket=websocket)


async def send_to_stream(room_id: str, websocket: WebSocket, service: WebsocketService):
    while True:
        message: str = await websocket.receive_text()
        await service.stream_message(room_id=room_id, message=message, websocket=websocket)

async def read_video_from_stream(room_id: str, service: WebsocketService, websocket: WebSocket, user: CustomUser, actual_time: float):
    while True:
        await service.update_user_room_time(room_id=room_id, actual_time=actual_time)


async def stream_video_message(room_id: str, websocket: WebSocket, service: WebsocketService, user: CustomUser, actual_time: float):
    while True:
        msg = jsonable_encoder({"actual_time":actual_time})
        await websocket.send_json(msg)


@app.websocket("/ws/{room_id}/chat")
@ws_room_permission()
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    service: WebsocketService = Depends(get_ws_service),
):
    await service.connect(websocket)
    read = asyncio.create_task(read_from_stream(service=service, websocket=websocket, room_id=room_id))
    write = asyncio.create_task(send_to_stream(service=service, websocket=websocket, room_id=room_id))

    try:
        await asyncio.gather(read, write)
    except WebSocketDisconnect:
        await service.disconnect(room_id=room_id, websocket=websocket)


@app.websocket("/ws/{room_id}/roll")
@ws_room_permission()
async def websocket_endpoint_roll(
    websocket: WebSocket,
    room_id: str,
    actual_time: float,
    # user: CustomUser = Depends(JWTBearer()),
    service: WebsocketService = Depends(get_ws_service),
):
    await service.connect(websocket)
    read = asyncio.create_task(read_video_from_stream(service=service, websocket=websocket, room_id=room_id, actual_time=actual_time))
    write = asyncio.create_task(stream_video_message(service=service, websocket=websocket, room_id=room_id, actual_time=actual_time))

    try:
        await asyncio.gather(read, write)
    except WebSocketDisconnect:
        await service.disconnect(room_id=room_id, websocket=websocket)


if __name__ == "__main__":
    uvicorn.run(
        "websocket:app",
        host=settings.PROJECT_HOST,
        port=settings.WS_PORT,
    )
