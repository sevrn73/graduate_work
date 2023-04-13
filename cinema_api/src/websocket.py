import asyncio
import logging
from functools import lru_cache
from http import HTTPStatus

import httpx
import jwt
import uvicorn
from aioredis import Redis
from connection_events.events import on_shutdown, on_startup
from connection_events.postgres import get_pg_engine
from connection_events.redis import get_redis_client
from core.auth.decorators import ws_room_permission
from core.auth.middleware import JWTBearer
from core.auth.models import CustomUser
from core.config import settings
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from services.ws import WebsocketService
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.authentication import AuthCredentials, AuthenticationBackend, SimpleUser
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

logger = logging.getLogger(__name__)


class ExtendedSimpleUser(SimpleUser):
    def __init__(self, username: str, first_name: str, last_name: str) -> None:
        super().__init__(username)
        self.pk = username
        self.first_name = first_name
        self.last_name = last_name


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.cookies:
            return
        auth = conn.cookies["Authorization"]
        scheme, credentials = auth.split()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.VERIFY_JWT_URL,
                headers={"Authorization": "Bearer " + credentials},
            )
        if response.status_code == HTTPStatus.OK:
            jwt_decoded = jwt.decode(credentials, algorithms="HS256", options={"verify_signature": False})
            return AuthCredentials(["authenticated"]), ExtendedSimpleUser(
                username=jwt_decoded["sub"],
                first_name=jwt_decoded["first_name"],
                last_name=jwt_decoded["last_name"],
            )


middleware = [Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())]

app = FastAPI(
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    middleware=middleware,
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


async def read_video_from_stream(
    room_id: str, service: WebsocketService, websocket: WebSocket, user: CustomUser, actual_time: float
):
    while True:
        await service.update_user_room_time(room_id=room_id, actual_time=actual_time)


async def stream_video_message(
    room_id: str, websocket: WebSocket, service: WebsocketService, user: CustomUser, actual_time: float
):
    while True:
        msg = jsonable_encoder({"actual_time": actual_time})
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
    read = asyncio.create_task(
        read_video_from_stream(service=service, websocket=websocket, room_id=room_id, actual_time=actual_time)
    )
    write = asyncio.create_task(
        stream_video_message(service=service, websocket=websocket, room_id=room_id, actual_time=actual_time)
    )

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
