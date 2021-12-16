from contextlib import contextmanager
from http import HTTPStatus

from fastapi.concurrency import contextmanager_in_threadpool
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from watch_n_learn.authentication.main import get_user, remove_authentication
from watch_n_learn.database.main import create_session
from watch_n_learn.database.models import Post
from watch_n_learn.helper.parse import body_as_json
from watch_n_learn.helper.template import flash

user_post_router = APIRouter(prefix="/internal")

@user_post_router.post("/post")
async def post(request: Request) -> RedirectResponse:

    body = await body_as_json(request, ["title", "content"])

    print(body)

    user = await get_user(request)

    if user is None:

        return remove_authentication(RedirectResponse("/", HTTPStatus.FOUND))

    title_ = body.get("title")

    content_ = body.get("content")

    if not 1 <= len(title_) <= 256:
        flash(request, "Title should be between 1 and 256 characters")
    elif not 16 <= len(content_) <= 4096:
        flash(request, "Content should be between 16 and 4096 characters")
    else:
        flash(request, "Posted message")
        async with contextmanager_in_threadpool(
            contextmanager(create_session)()
        ) as session:
            session.add(Post(user_id=user.id_, title=title_, content=content_))
            session.commit()

        return RedirectResponse("/explore", HTTPStatus.FOUND)

    return RedirectResponse("/post", HTTPStatus.FOUND)

@user_post_router.post("/edit/{id}")
async def edit_post(request: Request):
    
    body = await body_as_json(request, ["title", "text"])

    if body is None:

        return RedirectResponse("/", HTTPStatus.FOUND)

    title_ = body.get("title")
    
    text_ = body.get("text")
    
    user = await get_user(request)

    if user is None:
        flash(request, "Please sign in first")

        return remove_authentication(
            RedirectResponse("/sign-in", HTTPStatus.FOUND)
        )
        
    id_ = request.path_params.get("id")
    
    async with contextmanager_in_threadpool(
        contextmanager(create_session)()
    ) as session:
        
        post = session.query(Post).filter_by(id_ = id_).first()
        
        if user.id_ != post.user.id_:

            flash(request, "Only edit a post you own")

            return RedirectResponse("/", HTTPStatus.FOUND)
    
    if not 1 <= len(title_) <= 256:
        flash(request, "Title should be between 1 and 256 characters")
    elif not 16 <= len(text_) <= 4096:
        flash(request, "Content should be between 16 and 4096 characters")
    else: 
        async with contextmanager_in_threadpool(
            contextmanager(create_session)()
        ) as session:
            
            post = session.query(Post).filter_by(id_ = id_).first()
            
            post.title = title_
            post.content = text_
        
            session.commit()
        
            flash(request, "Post Edited")
        
    return RedirectResponse("/", HTTPStatus.FOUND)
