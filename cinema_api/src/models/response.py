from typing import List

from models.base import BaseModel


class ResponseModel(BaseModel):
    success: bool
    errors: List[str] = []
    data: dict = {}
