import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select

from app.models.feed import Feed, FeedPublic, FeedBase, FeedUpdate
from ..dependencies import get_session

router = APIRouter(
    prefix="/feeds",
    tags=["feeds"],
    responses={404: {"description": "Not found"}}, )


@router.get("/", response_model=list[FeedPublic], summary="Get all feeds")
async def get_feeds(
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
    feeds = session.exec(select(Feed).offset(offset).limit(limit)).all()
    return feeds


@router.post("/", response_model=FeedPublic, summary="Create feed")
async def add_feed(feed: FeedBase, session: Session = Depends(get_session)):
    feed_db = Feed.model_validate(feed)
    session.add(feed_db)
    session.commit()
    session.refresh(feed_db)
    return feed_db


@router.get("/{feed_id}", response_model=FeedPublic, summary="Get feed")
async def get_feed(feed_id: uuid.UUID, session: Session = Depends(get_session)):
    feed = session.get(Feed, feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="feed not found")
    return feed


@router.patch("/{feed_id}", response_model=FeedPublic, summary="Update feed")
async def update_feed(feed_id: uuid.UUID, feed: FeedUpdate, session: Session = Depends(get_session)):
    feed_db = session.get(Feed, feed_id)
    if not feed_db:
        raise HTTPException(status_code=404, detail="feed not found")
    feed_data = feed.model_dump(exclude_unset=True)
    feed_db.sqlmodel_update(feed_data)
    session.add(feed_db)
    session.commit()
    session.refresh(feed_db)
    return feed_db


@router.delete("/{feed_id}", summary="Delete feed")
def delete_feed(feed_id: uuid.UUID, session: Session = Depends(get_session)):
    feed_db = session.get(Feed, feed_id)
    if not feed_db:
        raise HTTPException(status_code=404, detail="feed not found")
    session.delete(feed_db)
    session.commit()
    return {"ok": True}
