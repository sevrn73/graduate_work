from models.base import BaseModel
from pydantic.validators import UUID


class UserModel(BaseModel):
    id: UUID
    first_name: str
    last_name: str
