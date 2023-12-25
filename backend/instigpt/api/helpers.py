import datetime
from typing import Annotated
from fastapi import Cookie, HTTPException

from instigpt import config
from instigpt.db import session as db_session, user as db_user


async def get_user(
    session_id: Annotated[str | None, Cookie(alias=config.COOKIE_NAME)] = None
) -> db_user.User:
    if session_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    session = db_session.get_by_id(session_id)
    if session is None or session.expires_at < datetime.datetime.now():
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = db_user.get_user_by_id(session.user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user
