from http import HTTPStatus
from typing import List, Optional

from core.auth.middleware import JWTBearer
from core.auth.models import CustomUser
from fastapi import APIRouter, Depends, HTTPException
from models.response import ResponseModel
from models.room import RoomModel, RoomUserModel, RoomUserTypeModel
from pydantic.validators import UUID
from services.room import RoomService, get_room_service

room_router = APIRouter()


@room_router.get("/", response_model=RoomModel)
async def get_owner_room(
    user: CustomUser = Depends(JWTBearer()),
    service: RoomService = Depends(get_room_service),
) -> Optional[RoomModel]:
    room = await service.get_owner_room(user=user)
    if not room:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User room not found!")
    return room


@room_router.post("/{film_work_uuid}", response_model=ResponseModel)
async def create_room(
    film_work_uuid: str,
    user: CustomUser = Depends(JWTBearer()),
    service: RoomService = Depends(get_room_service),
) -> ResponseModel:
    error = await service.create_user_room(user_id=user.pk, film_work_uuid=film_work_uuid)
    if error:
        return ResponseModel(success=False, errors=[error])

    room = await service.get_owner_room(user=user)
    if not room:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User room not found!")
    return ResponseModel(success=True, data={"room_id": room.id})


@room_router.delete("/delete", response_model=ResponseModel)
async def delete_room(
    user: CustomUser = Depends(JWTBearer()),
    service: RoomService = Depends(get_room_service),
) -> ResponseModel:
    status = await service.delete_room(user=user)
    if status:
        return ResponseModel(success=False, errors=[status])
    return ResponseModel(success=True)


@room_router.get("/users", response_model=List[RoomUserModel])
async def get_room_users(
    user: CustomUser = Depends(JWTBearer()),
    service: RoomService = Depends(get_room_service),
) -> List[RoomUserModel]:
    return await service.get_room_users(user=user)


@room_router.get("/rooms", response_model=List[RoomModel])
async def get_rooms(
    user: CustomUser = Depends(JWTBearer()),
    service: RoomService = Depends(get_room_service),
) -> List[RoomModel]:
    return await service.get_rooms(user=user)


@room_router.post("/{room_id}/join", response_model=ResponseModel)
async def join(
    room_id: UUID,
    user: CustomUser = Depends(JWTBearer()),
    service: RoomService = Depends(get_room_service),
) -> ResponseModel:
    error = await service.join(
        user=user,
        room_id=str(room_id),
    )
    if error:
        return ResponseModel(success=False, errors=[error])
    return ResponseModel(success=True)


@room_router.post("/{user_id}/invite", response_model=ResponseModel)
async def invite(
    user_id: UUID,
    user: CustomUser = Depends(JWTBearer()),
    service: RoomService = Depends(get_room_service),
) -> ResponseModel:
    error = await service.invite(user=user, user_id=str(user_id))
    if error:
        return ResponseModel(success=False, errors=[error])
    return ResponseModel(success=True)


@room_router.get("/{room_id}", response_model=RoomModel)
async def get_room(
    room_id: UUID,
    user: CustomUser = Depends(JWTBearer()),
    service: RoomService = Depends(get_room_service),
) -> RoomModel:
    room = await service.get_room(user=user, room_id=room_id)
    if not room:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permission denied!")
    return room
