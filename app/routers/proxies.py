import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.models.feed import Feed
from ..dependencies import get_session
from ..models.diun import DiunNotification, create_feeditem
from ..models.feeditem import FeedItemPublic

router = APIRouter(
    prefix="/feeds/{feed_id}",
    tags=["proxies"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/diun/",
    response_model=FeedItemPublic,
    summary="add feed item from diun webhook call",
)
async def create_diun_feeditem(
        feed_id: uuid.UUID, notif: DiunNotification,
        session: Session = Depends(get_session)
):
    feed = session.get(Feed, feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="feed not found")
    feeditem = await create_feeditem(feed_id, notif, session)
    return feeditem
