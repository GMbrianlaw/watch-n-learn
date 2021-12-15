from contextlib import contextmanager
from sys import version_info
from typing import Optional, TypeVar

from fastapi.concurrency import contextmanager_in_threadpool
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi_login.fastapi_login import LoginManager

from watch_n_learn.database.main import DatabaseSession, create_session
from watch_n_learn.database.models import User
from watch_n_learn.helper.environment import FASTAPI_LOGIN_TOKEN_VALUE

FASTAPI_LOGIN_COOKIE_NAME = "watch_n_learn-authentication-token"

_BaseResponse = TypeVar("_BaseResponse", bound=Response)

login_manager = LoginManager(
    FASTAPI_LOGIN_TOKEN_VALUE, "/internal/sign-in",
    cookie_name=FASTAPI_LOGIN_COOKIE_NAME
)

@login_manager.user_loader()
async def load_user(username: str) -> Optional[User]:

    async with contextmanager_in_threadpool(
        contextmanager(create_session)()
    ) as session:

        return session.query(User).filter_by(username=username).first()

if version_info.minor <= 7:
    # Synchronous version because 3.7 has issues (dev in school)
    @login_manager.user_loader()
    def load_user_synchronous(username: str) -> Optional[User]:

        return DatabaseSession().query(User).filter_by(username=username).first(
        )

async def get_user(request: Request) -> Optional[User]:

    try:

        return await login_manager.get_current_user(
            request.cookies.get(FASTAPI_LOGIN_COOKIE_NAME)
        )

    except HTTPException:

        return None

def remove_authentication(response: _BaseResponse) -> _BaseResponse:

    # Mutating response is fine, it is immediately returned
    response.delete_cookie(FASTAPI_LOGIN_COOKIE_NAME)

    return response
