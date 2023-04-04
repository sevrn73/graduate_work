import datetime
import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Room(Base):
    __tablename__ = "cinema_together_room"

    created_at = Column(DateTime, default=datetime.datetime.now())
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    owner_uuid = Column(UUID, nullable=False, unique=True)

    film_work_uuid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    film_work_time = Column(Float, nullable=True)
    film_work_state = Column(String, nullable=True)

    room_users = relationship("RoomUser")

    __mapper_args__ = {"eager_defaults": True}


class RoomUser(Base):
    __tablename__ = "cinema_together_room_user"

    created_at = Column(DateTime, default=datetime.datetime.now())

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_uuid = Column(UUID(as_uuid=True))
    user_type = Column(String)

    room_uuid = Column(ForeignKey("cinema_together_room.id"))

    __table_args__ = (UniqueConstraint("user_uuid", "room_uuid", name="unique_room_user"),)
