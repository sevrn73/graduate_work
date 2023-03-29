import functools

from fastapi import status
from pydantic.validators import UUID
from services.ws import WebsocketService

__all__ = "ws_room_permission"


def ws_room_permission():
    def wrapper(func):
        @functools.wraps(func)
        async def inner(*args, **kwargs):
            websocket = kwargs.get("websocket")
            if not websocket or not websocket.user.is_authenticated:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return None

            service: WebsocketService = kwargs.get("service")
            room_id: UUID = kwargs.get("room_id")
            room = await service.get_room(room_id=room_id, user=websocket.user)
            if not room:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return None

            return await func(*args, **kwargs)

        return inner

    return wrapper
