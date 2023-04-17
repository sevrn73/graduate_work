import logging
from functools import lru_cache
from typing import List, Optional
from uuid import UUID

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine

from connection_events.postgres import get_pg_engine
from connection_events.redis import get_redis_client
from core.auth.models import CustomUser
from models.db.room import Room, RoomUser
from models.room import RoomModel, RoomUserModel, RoomUserTypeEnum
from services.base import BaseService

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

    async def create_user_room(self, user_id: str, film_work_uuid: str):
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

    async def delete_room(self, user: CustomUser):
        async with self.db_connection.begin() as conn:
            room = await conn.execute(select(Room).where(Room.owner_uuid == str(user.pk)))
            room_obj = room.mappings().fetchone()

            if room_obj:
                await conn.execute(delete(RoomUser).where(RoomUser.room_uuid == str(room_obj["id"])))
                await conn.execute(delete(Room).where(Room.id == str(room_obj["id"])))
            else:
                return f"Room does not exist!"

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

            room = await conn.execute(select(Room).where(Room.id == str(room_id)))
            existed_room = room.mappings().fetchone()
            return RoomModel(**existed_room) if existed_room else None

    async def invite(self, user: CustomUser, user_id: str) -> Optional[str]:
        async with self.db_connection.begin() as conn:
            room = await conn.execute(select(Room).where(Room.owner_uuid == user.pk))
            room_obj = room.mappings().fetchone()

            if not room_obj:
                return f"Room does not exist!"

            if user.pk != str(room_obj["owner_uuid"]):
                return f'You are not the owner of the room {room_obj["id"]}!'

            try:
                await conn.execute(
                    insert(RoomUser).values(
                        room_uuid=str(room_obj["id"]),
                        user_uuid=user_id,
                        user_type=RoomUserTypeEnum.pending.value,
                    )
                )
            except IntegrityError as exc:
                logger.error(exc)
                return f'Room user "{user_id}" already exist!'

    async def join(
        self,
        user: CustomUser,
        room_id: str,
    ) -> Optional[str]:
        async with self.db_connection.begin() as conn:
            room = await conn.execute(select(Room.owner_uuid).where(Room.id == room_id))
            room_owner = room.scalars().first()
            if user.pk == room_owner:
                return
            await conn.execute(
                update(RoomUser)
                .where(and_(RoomUser.room_uuid == room_id, RoomUser.user_uuid == user.pk))
                .values(user_type=RoomUserTypeEnum.member.value)
            )

    async def get_room_users(self, user: CustomUser) -> List[RoomUserModel]:
        async with self.db_connection.begin() as conn:
            room = await conn.execute(select(Room.id).where(Room.owner_uuid == user.pk))
            room_id = room.scalars().first()

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
