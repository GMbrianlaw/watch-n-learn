from contextlib import contextmanager
from http import HTTPStatus

from fastapi.concurrency import contextmanager_in_threadpool
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from watch_n_learn.authentication.main import get_user, remove_authentication
from watch_n_learn.database.main import create_session
from watch_n_learn.database.models import Post, User
from watch_n_learn.helper.template import (
    RedirectOrTemplate, TemplateResponse, flash
)

user_get_router = APIRouter()

@user_get_router.get("/explore")
async def explore(request: Request) -> RedirectOrTemplate:

    user = await get_user(request)

    if user is None:
        flash(request, "Sign in to explore posts")

        return remove_authentication(
            RedirectResponse("/sign-in", HTTPStatus.FOUND)
        )

    async with contextmanager_in_threadpool(
        contextmanager(create_session)()
    ) as session:
        recent_posts = session.query(Post).filter_by(isdeleted = False).order_by(Post.time.desc()).limit(
            10
        ).all()

    return TemplateResponse(
        "user/explore.jinja2",
        {"request": request, "user": user, "recent_posts": recent_posts}
    )

@user_get_router.get("/post")
async def post_(request: Request) -> RedirectOrTemplate:

    user = await get_user(request)

    if user is None:
        flash(request, "Sign in to post")

        return remove_authentication(
            RedirectResponse("/sign-in", HTTPStatus.FOUND)
        )

    return TemplateResponse(
        "user/post.jinja2", {"request": request, "user": user}
    )

@user_get_router.get("/user/{username}")
async def user_(request: Request) -> RedirectOrTemplate:

    user = await get_user(request)

    if user is None:
        flash(request, "Sign in to view profiles")

        return remove_authentication(
            RedirectResponse("/sign-in", HTTPStatus.FOUND)
        )

    username_ = request.path_params.get("username")

    async with contextmanager_in_threadpool(
        contextmanager(create_session)()
    ) as session:

        return TemplateResponse(
            "user/user.jinja2",
            {
                "request": request, "user": user,
                "view_user": session.query(User).filter_by(
                    username=username_
                ).first()
            }
        )

@user_get_router.get("/view/{id}")
async def view(request: Request) -> RedirectOrTemplate:

    user = await get_user(request)

    if user is None:
        flash(request, "Sign in to view post")

        return remove_authentication(
            RedirectResponse("/sign-in", HTTPStatus.FOUND)
        )

    id_ = request.path_params.get("id")

    async with contextmanager_in_threadpool(
        contextmanager(create_session)()
    ) as session:
        
        post = session.query(Post).filter_by(id_ = id_).first()
        
        if post.isdeleted == True:
            
            return RedirectResponse("/", HTTPStatus.FOUND)
        
            flash(request, "post is deleted")
        
        if user.id_ != post.user.id_:

            return TemplateResponse(
                "user/view.jinja2",
                {
                    "request": request, "user": user,
                    "post": post
                }
            )
        else:
            
            return TemplateResponse(
                "user/yourpost.jinja2",
                {
                    "request": request, "user": user,
                    "post": post
                }
            )
        
@user_get_router.get("/delete/{id}")
async def delete(request: Request) -> RedirectOrTemplate:
    
    id_ = request.path_params.get("id")
    
    async with contextmanager_in_threadpool(
        contextmanager(create_session)()
    ) as session:
        
        post = session.query(Post).filter_by(id_ = id_).first()
        
        post.isdeleted = True
    
        session.commit()
        
    flash(request, "Post Deleted")
    
    return RedirectResponse("/explore", HTTPStatus.FOUND)
