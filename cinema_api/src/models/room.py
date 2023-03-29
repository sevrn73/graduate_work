from enum import Enum
from typing import Optional

from models.base import BaseModel
from pydantic.validators import UUID, datetime


class RoomUserMessageTypeEnum(str, Enum):
    service = "service"
    user = "user"


class RoomUserTypeEnum(str, Enum):
    pending = "pending"
    member = "member"
    owner = "owner"


class RoomModel(BaseModel):
    id: UUID
    owner_uuid: UUID
    film_work_uuid: Optional[UUID] = None
    film_work_time: Optional[float] = None
    film_work_state: Optional[str] = None


class RoomUserModel(BaseModel):
    id: Optional[UUID] = None
    room_uuid: UUID
    user_uuid: UUID
    user_type: RoomUserTypeEnum
    created_at: datetime

    class Config:
        use_enum_values = True


class RoomUserTypeModel(BaseModel):
    user_type: RoomUserTypeEnum


class RoomUserMessage(BaseModel):
    text: str
    msg_type: RoomUserMessageTypeEnum
    user_id: Optional[UUID] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        use_enum_values = True
