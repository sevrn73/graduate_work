from api.v1.routers import api_v1_router
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(api_v1_router, prefix="/cinema_v1")
