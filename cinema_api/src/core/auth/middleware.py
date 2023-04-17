import logging
from http import HTTPStatus

import httpx
import jwt
from core.auth.models import CustomUser
from core.config import settings
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        custom_logger = logging.LoggerAdapter(
            logger, extra={"tags": ["api"], "request_id": request.headers.get("X-Request-Id")}
        )
        custom_logger.info(request)

        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid authentication scheme.")

            is_token_valid = await self.verify_jwt(credentials.credentials) if settings.verify_jwt_mode else True
            if not is_token_valid:
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token or expired token.")

            jwt_decoded = jwt.decode(credentials.credentials, algorithms="HS256", options={"verify_signature": False})
            try:
                auth_user = CustomUser(
                    pk=jwt_decoded["sub"],
                    first_name=jwt_decoded["first_name"],
                    last_name=jwt_decoded["last_name"],
                )
            except KeyError:
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Bad signature for user")

            return auth_user
        else:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid authorization code.")

    async def verify_jwt(self, jwtoken: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.verify_jwt_url, headers={"Authorization": "Bearer " + jwtoken})
        if response.status_code == HTTPStatus.OK:
            return True
        else:
            return False
