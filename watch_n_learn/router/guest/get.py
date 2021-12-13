from http import HTTPStatus

from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter
from starlette.templating import _TemplateResponse

from watch_n_learn.authentication.main import get_user, remove_authentication
from watch_n_learn.database.models import User
from watch_n_learn.helper.template import (
    RedirectOrTemplate, TemplateResponse, flash
)

guest_get_router = APIRouter()

@guest_get_router.get("/")
async def index(request: Request) -> _TemplateResponse:

    user = await get_user(request)

    if isinstance(user, User):

        return TemplateResponse(
            "user/index.jinja2", {"request": request, "user": user}
        )

    return remove_authentication(
        TemplateResponse("guest/index.jinja2", {"request": request})
    )

@guest_get_router.get("/sign-in")
async def sign_in(request: Request) -> RedirectOrTemplate:

    user = await get_user(request)

    if isinstance(user, User):

        return RedirectResponse("/", HTTPStatus.FOUND)

    return remove_authentication(
        TemplateResponse("guest/sign_in.jinja2", {"request": request})
    )

@guest_get_router.get("/sign-out")
async def sign_out(request: Request) -> RedirectResponse:

    user = await get_user(request)

    if isinstance(user, User):
        flash(request, "You have signed out")

    return remove_authentication(RedirectResponse("/", HTTPStatus.FOUND))

@guest_get_router.get("/register")
async def register(request: Request) -> RedirectOrTemplate:

    user = await get_user(request)

    if isinstance(user, User):

        return RedirectResponse("/", HTTPStatus.FOUND)

    return remove_authentication(
        TemplateResponse("guest/register.jinja2", {"request": request})
    )
