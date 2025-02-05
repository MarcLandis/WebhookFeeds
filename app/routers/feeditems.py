import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select

from app.models.feed import Feed
from app.models.feeditem import FeedItem, FeedItemBase, FeedItemPublic, FeedItemUpdate
from ..dependencies import get_session

router = APIRouter(
    prefix="/feeds/{feed_id}",
    tags=["feed items"],
    responses={404: {"description": "Not found"}}, )


@router.get("/feeditems/", response_model=list[FeedItemPublic],
            summary="Get feed items for a feed")
async def get_feeditems(feed_id: uuid.UUID, session: Session = Depends(get_session), offset: int = 0,
                        limit: Annotated[int, Query(le=100)] = 100):
    feed = session.get(Feed, feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="feed not found")
    feeditems = session.exec(select(FeedItem).where(FeedItem.feed_id == feed_id).offset(offset).limit(limit)).all()
    return feeditems


@router.post("/feeditems/", response_model=FeedItemPublic,
             summary="Create feed item")
async def add_feeditem(feed_id: uuid.UUID, feeditem: FeedItemBase, session: Session = Depends(get_session),
                       insert_or_update: bool = True):
    feed = session.get(Feed, feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="feed not found")
    feeditem_db = session.exec(
        select(FeedItem).where(FeedItem.feed_id == feed_id).where(FeedItem.guid == feeditem.guid)).first()
    if insert_or_update:
        if feeditem_db:
            return await update_feeditem(feeditem, feeditem_db, session)
        else:
            return await create_feeditem(feed_id, feeditem, session)
    else:
        if feeditem_db:
            raise HTTPException(status_code=409, detail="feed item already exists")
        else:
            return await create_feeditem(feed_id, feeditem, session)


@router.get("/feeditems/{feeditem_id}", response_model=FeedItemPublic,
            summary="Get feed item")
async def get_feeditems_by_feed_id(feed_id: uuid.UUID, feeditem_id: uuid.UUID, session: Session = Depends(get_session),
                                   offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    feed = session.get(Feed, feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="feed not found")
    feeditem = session.exec(
        select(FeedItem).where(FeedItem.feed_id == feed_id).where(FeedItem.id == feeditem_id).offset(offset).limit(
            limit)).first()
    if not feeditem:
        raise HTTPException(status_code=404, detail="feed item not found")
    return feeditem


@router.patch("/feeditems/{feeditem_id}", response_model=FeedItemPublic,
              summary="Update feed item")
async def patch_feeditem(feed_id: uuid.UUID, feeditem_id: uuid.UUID, feeditem: FeedItemUpdate,
                         session: Session = Depends(get_session)):
    feed = session.get(Feed, feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="feed not found")
    feeditem_db = session.exec(
        select(FeedItem).where(FeedItem.feed_id == feed_id).where(FeedItem.id == feeditem_id)).first()
    if not feeditem_db:
        raise HTTPException(status_code=404, detail="feed item not found")
    return await update_feeditem(feeditem, feeditem_db, session)


@router.delete("/feeditems/{feeditem_id}", summary="Delete feed item")
def delete_feeditem(feed_id: uuid.UUID, feeditem_id: uuid.UUID, session: Session = Depends(get_session)):
    feed = session.get(Feed, feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="feed not found")
    feeditem_db = session.exec(
        select(FeedItem).where(FeedItem.feed_id == feed_id).where(FeedItem.id == feeditem_id)).first()
    if not feeditem_db:
        raise HTTPException(status_code=404, detail="feed item not found")
    session.delete(feeditem_db)
    session.commit()
    return {"ok": True}


async def create_feeditem(feed_id, feeditem, session):
    extra_data = {"feed_id": feed_id}
    feeditem = feeditem
    feeditem_db = FeedItem.model_validate(feeditem, update=extra_data)
    session.add(feeditem_db)
    session.commit()
    session.refresh(feeditem_db)
    return feeditem_db


async def update_feeditem(feeditem, feeditem_db, session):
    feeditem_data = feeditem.model_dump(exclude_unset=True)
    feeditem_db.sqlmodel_update(feeditem_data)
    session.add(feeditem_db)
    session.commit()
    session.refresh(feeditem_db)
    return feeditem_db
