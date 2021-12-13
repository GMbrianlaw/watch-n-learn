from http import HTTPStatus

from fastapi.applications import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import _TemplateResponse

from watch_n_learn.database.models import Base
from watch_n_learn.helper.environment import SESSION_MIDDLEWARE_TOKEN_NAME
from watch_n_learn.helper.template import template
from watch_n_learn.router.guest.get import guest_get_router
from watch_n_learn.router.guest.post import guest_post_router
from watch_n_learn.router.user.get import user_get_router
from watch_n_learn.router.user.post import user_post_router

def create_server(debug_: bool) -> FastAPI:

    Base.metadata.create_all()

    server = FastAPI(debug=debug_, openapi_url=None)

    server.add_middleware(
        SessionMiddleware, secret_key=SESSION_MIDDLEWARE_TOKEN_NAME
    )

    server.include_router(guest_get_router)
    server.include_router(guest_post_router)

    server.include_router(user_get_router)
    server.include_router(user_post_router)

    server.mount("/static", StaticFiles(directory="watch_n_learn/static"))

    @server.get("/ping")
    @server.head("/ping")
    async def ping() -> None:

        return None

    @server.get("/{_:path}")
    async def not_found(request: Request) -> _TemplateResponse:

        return template.TemplateResponse(
            "not_found.jinja2", {"request": request}, HTTPStatus.NOT_FOUND
        )

    return server
