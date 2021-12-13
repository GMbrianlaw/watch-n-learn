from contextvars import ContextVar
from typing import List, Union

from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

REQUEST_CONTEXT = ContextVar("request_context", default=None)

RedirectOrTemplate = Union[RedirectResponse, _TemplateResponse]

template = Jinja2Templates("watch_n_learn/template")

def flash(request: Request, message_: str) -> None:

    request.session["_flashes"] = request.session.get(
        "_flashes", []
    ) + [message_]

def get_flashed_messages(request: Request) -> List[str]:

    flashed_messages = REQUEST_CONTEXT.get()

    if flashed_messages is None:
        flashed_messages = request.session.pop("_flashes", [])
        REQUEST_CONTEXT.set(flashed_messages)

    return flashed_messages

template.env.globals["get_flashed_messages"] = get_flashed_messages

TemplateResponse = template.TemplateResponse
