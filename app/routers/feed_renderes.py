import uuid

import feedendum
from fastapi import APIRouter, Depends, HTTPException, Response
from feedendum import rss, atom
from sqlmodel import Session, select

from app.models.feed import Feed
from app.models.feeditem import FeedItem
from ..dependencies import get_session

router = APIRouter(
    prefix="/feeds/{feed_id}",
    tags=["feed renderer"],
    responses={404: {"description": "Not found"}}, )


@router.get("/rssfeed/", response_class=Response, summary="Get RSS feed")
async def get_rssfeed(feed_id: uuid.UUID, session: Session = Depends(get_session)):
    feed = session.get(Feed, feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="feed not found")
    data: str = generate_feed(feed_id, session)
    return Response(content=data, media_type="application/xml")


@router.get("/atomfeed/", response_class=Response, summary="Get Atom feed")
async def get_atomfeed(feed_id: uuid.UUID, session: Session = Depends(get_session)):
    feed = session.get(Feed, feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="feed not found")
    data: str = generate_feed(feed_id, session, "atom")
    return Response(content=data, media_type="application/xml")


def generate_feed(feed_id: uuid.UUID, session: Session = Depends(get_session), feed_type: str = "rss"):
    feed_db = session.get(Feed, feed_id)
    if not feed_db:
        raise HTTPException(status_code=404, detail="feed not found")
    feeditems_db = session.exec(select(FeedItem).where(FeedItem.feed_id == feed_id)).all()
    feed: feedendum.Feed = feedendum.Feed(title=feed_db.title, url=feed_db.link, description=feed_db.description,
                                          update=feed_db.pubDate)
    for feeditem_db in feeditems_db:
        feeditem = feedendum.FeedItem(title=feeditem_db.title, url=feeditem_db.link, content=feeditem_db.description,
                                      update=feeditem_db.pubDate, id=feeditem_db.guid)
        feed.items.append(feeditem)

    data: str = ""

    if feed_type == "rss":
        data = rss.generate(feed)
    elif feed_type == "atom":
        data = atom.generate(feed)

    return data
