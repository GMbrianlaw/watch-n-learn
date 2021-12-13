from contextlib import contextmanager
from http import HTTPStatus
from string import ascii_letters, digits, punctuation

from bcrypt import checkpw, gensalt, hashpw
from fastapi.concurrency import contextmanager_in_threadpool
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from watch_n_learn.authentication.main import get_user, load_user, login_manager
from watch_n_learn.database.main import create_session
from watch_n_learn.database.models import User
from watch_n_learn.helper.parse import body_as_json
from watch_n_learn.helper.template import flash

ALLOWED_NAME_CHARACTERS = frozenset(ascii_letters + " ")

ALLOWED_USERNAME_CHARACTERS = frozenset(ascii_letters + digits+_punctuation+"_")

_punctuation = punctuation

_punctuation.replace("\\", "")

ALLOWED_PASSWORD_CHARACTERS = frozenset(ascii_letters + digits + _punctuation)

guest_post_router = APIRouter(prefix="/internal")

@guest_post_router.post("/sign-in")
async def sign_in(request: Request) -> RedirectResponse:

    body = await body_as_json(request, ["username", "password"])

    if body is None:

        return RedirectResponse("/sign-in", HTTPStatus.FOUND)

    user = await get_user(request)

    if isinstance(user, User):

        return RedirectResponse("/", HTTPStatus.FOUND)

    username = body.get("username")

    password = body.get("password")

    user_ = await load_user(username)

    if user_ is None:
        flash(request, "Username not found")
    elif not checkpw(password.encode("utf-8"), user_.hashed_password):
        flash(request, "Incorrect password")
    else:
        flash(request, "You have signed in")
        response = RedirectResponse("/", HTTPStatus.FOUND)
        login_manager.set_cookie(
            response, login_manager.create_access_token(data={"sub": username})
        )

        return response

    return RedirectResponse("/sign-in", HTTPStatus.FOUND)

@guest_post_router.post("/register")
async def register(request: Request) -> RedirectResponse:

    body = await body_as_json(
        request, ["name", "username", "password", "confirm_password"]
    )

    user = await get_user(request)

    if body is None:

        return RedirectResponse("/register", HTTPStatus.FOUND)

    if isinstance(user, User):

        return RedirectResponse("/", HTTPStatus.FOUND)

    name_ = body.get("name")

    username_ = body.get("username")

    password = body.get("password")

    for character in name_:
        if character not in ALLOWED_NAME_CHARACTERS:
            flash(request, "Name can only contain characters and spaces")
            return RedirectResponse("/register", HTTPStatus.FOUND)

    for character in username_:
        if character not in ALLOWED_USERNAME_CHARACTERS:
            flash(request, "Username can only contain characters, digits, punctuation, and the '_' character")
            return RedirectResponse("/register", HTTPStatus.FOUND)

    for character in password:
        if character not in ALLOWED_PASSWORD_CHARACTERS:
            flash(
                request,
                "Password can only contain characters, digits and punctuation"
            )
            return RedirectResponse("/register", HTTPStatus.FOUND)

    if not 6 <= len(name_) <= 32:
        flash(request, "Full Name should be between 6 and 32 characters")
    elif not 6 <= len(username_) <= 16:
        flash(request, "Username should be between 6 and 16 characters")
    elif not 6 <= len(password) <= 32:
        flash(request, "Password should be between 6 and 32 characters")
    elif body.get("confirm_password") != password:
        flash(request, "Confirm Password should match Password")
    else:
        async with contextmanager_in_threadpool(
            contextmanager(create_session)()
        ) as session:
            if session.query(User).filter_by(
                username=username_
            ).first() is None:
                flash(request, "You have registered, sign in")
                session.add(
                    User(
                        name=name_, username=username_,
                        hashed_password=hashpw(
                            password.encode("utf-8"), gensalt()
                        )
                    )
                )
                session.commit()

                return RedirectResponse("/sign-in", HTTPStatus.FOUND)

            flash(request, "Username has been taken")

    return RedirectResponse("/register", HTTPStatus.FOUND)
