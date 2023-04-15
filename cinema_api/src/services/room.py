import logging
from functools import lru_cache
from typing import List, Optional
from uuid import UUID

from aioredis import Redis
from connection_events.postgres import get_pg_engine
from connection_events.redis import get_redis_client
from core.auth.models import CustomUser
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from models.db.room import Room, RoomUser
from models.room import RoomModel, RoomUserMessage, RoomUserMessageTypeEnum, RoomUserModel, RoomUserTypeEnum
from services.base import BaseService
from sqlalchemy import and_, exists, insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine

__all__ = ("get_room_service", "RoomService")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class RoomService(BaseService):
    async def get_owner_room(self, user: CustomUser) -> Optional[RoomModel]:
        async with self.db_connection.begin() as conn:
            room = await conn.execute(select(Room).where(Room.owner_uuid == str(user.pk)))
            existed_room = room.mappings().fetchone()
            return RoomModel(**existed_room) if existed_room else None

    async def update_user_room_time(self, room_id: str, actual_time: float):
        async with self.db_connection.begin() as conn:
            await conn.execute(update(Room).where(and_(Room.id == room_id)).values(film_work_time=actual_time))

    async def create_user_room(self, user_id: str, film_work_uuid:str):
        async with self.get_session() as session:
            try:
                async with session.begin():
                    session.add(
                        Room(
                            owner_uuid=user_id,
                            room_users=[RoomUser(user_uuid=user_id, user_type=RoomUserTypeEnum.owner.value)],
                            film_work_uuid=film_work_uuid,
                        )
                    )
            except IntegrityError as exc:
                logger.error(exc)
                return f'Room for user "{user_id}" already exist!'

    async def delete_room(self, room_id: UUID, user: CustomUser):
        async with self.db_connection.begin() as conn:
            room = await conn.execute(
                select(Room).where(and_(Room.id == str(room_id),Room.owner_uuid == str(user.pk))
            ))

            if room.first() is not None:
                await conn.execute(delete(RoomUser).where((RoomUser.room_uuid == str(room_id))))
                await conn.execute(delete(Room).where(and_(Room.id == str(room_id),Room.owner_uuid == str(user.pk))))
            return f'Room "{room_id}" does not exist!'

    async def get_room(self, room_id: UUID, user: CustomUser) -> Optional[RoomModel]:
        async with self.db_connection.begin() as conn:
            room_user_type = await conn.execute(
                select(RoomUser.user_type).where(
                    RoomUser.room_uuid == str(room_id),
                    RoomUser.user_uuid == str(user.pk),
                )
            )
            existed_room_user_type = room_user_type.scalars().first()
            if not existed_room_user_type or existed_room_user_type == RoomUserTypeEnum.pending.value:
                return None

            room = await conn.execute(select(Room).where(RoomUser.room_uuid == str(room_id)))
            existed_room = room.mappings().fetchone()
            return RoomModel(**existed_room) if existed_room else None

    async def invite(self, user: CustomUser, room_id: str, user_id: str) -> Optional[str]:
        async with self.db_connection.begin() as conn:
            room = await conn.execute(select(Room.owner_uuid).where(Room.id == room_id))
            room_owner = room.scalars().first()

            if not room_owner:
                return f'Room "{room_id}" does not exist!'

            if user.pk != room_owner:
                return f'You are not the owner of the room "{room_id}"!'

            try:
                await conn.execute(
                    insert(RoomUser).values(
                        room_uuid=room_id,
                        user_uuid=user_id,
                        user_type=RoomUserTypeEnum.pending.value,
                    )
                )
            except IntegrityError as exc:
                logger.error(exc)
                return f'Room user "{user_id}" already exist!'

    async def join(
        self,
        room_id: str,
        user_id: str,
    ) -> Optional[str]:
        async with self.db_connection.begin() as conn:
            await conn.execute(
                update(RoomUser)
                .where(and_(RoomUser.room_uuid == room_id, RoomUser.user_uuid == user_id))
                .values(user_type=RoomUserTypeEnum.member.value)
            )

    async def get_room_users(self, room_id: str) -> List[RoomUserModel]:
        async with self.db_connection.begin() as conn:
            results = await conn.execute(select(RoomUser).where(RoomUser.room_uuid == room_id))
            room_users = results.mappings().fetchall()
            return [RoomUserModel(**room_user) for room_user in room_users] if room_users else []

    async def get_rooms(self, user: CustomUser) -> List[RoomModel]:
        async with self.db_connection.begin() as conn:
            results = await conn.execute(select(RoomUser.room_uuid).where(RoomUser.user_uuid == user.pk))
            room_ids = results.mappings().fetchall()

            results = await conn.execute(select(Room).where(Room.id.in_([str(_["room_uuid"]) for _ in room_ids])))
            rooms = results.mappings().fetchall()
            return [RoomModel(**room) for room in rooms] if rooms else []


@lru_cache()
def get_room_service(
    db_connection: AsyncEngine = Depends(get_pg_engine),
    redis: Redis = Depends(get_redis_client),
) -> RoomService:
    return RoomService(db_connection, redis)
