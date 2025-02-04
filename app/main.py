import uuid
from contextlib import asynccontextmanager
from typing import Annotated

import cmarkgfm
import feedendum
import feedendum.atom as atom
import feedendum.rss as rss
from cmarkgfm.cmark import Options as cmarkgfmOptions
from fastapi import FastAPI, Depends, Query, HTTPException, Response
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from app.config import ASSETS_DIR
from app.database import create_db_and_tables, engine
from app.models import FeedPublic, Feed, FeedBase, FeedUpdate, FeedItemPublic, FeedItem, FeedItemBase, FeedItemUpdate
from app.util import get_root_folder


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(_):
    create_db_and_tables()
    yield
    # Clean up


description = """
### A simple RESTful API to create and get feeds
[MIT license](./LICENSE.md)
"""

tags_metadata = [
    {
        "name": "feeds",
        "description": "Manage feeds.",
    },
    {
        "name": "feed items",
        "description": "Manage feed items.",
    },
    {
        "name": "feed renderer",
        "description": "Render feeds.",
    },
]

app = FastAPI(lifespan=lifespan, title="Webhook Feeds", version="0.1.0", description=description, redoc_url=None,
              docs_url=None)
app.mount("/.assets", StaticFiles(directory=ASSETS_DIR), name=".assets")


@app.get("/", include_in_schema=False)
async def root():
    with open(get_root_folder() / 'README.md', 'r', encoding="utf-8") as f:
        md = f.read()
    template = """
    <html>
        <head>
            <title>Webhook Feeds</title>
            <link rel="icon" type="image/x-icon" href=".assets/favicon.ico">
        </head>
        <body>
            {content}
        </body>
    </html>
    """
    html_content = template.replace("{content}",
                                    cmarkgfm.github_flavored_markdown_to_html(md, options=(
                                            cmarkgfmOptions.CMARK_OPT_GITHUB_PRE_LANG
                                            | cmarkgfmOptions.CMARK_OPT_SMART
                                            | cmarkgfmOptions.CMARK_OPT_UNSAFE
                                    )))
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/LICENSE.md", include_in_schema=False)
async def get_license():
    with open(get_root_folder() / 'LICENSE.md', 'r', encoding="utf-8") as f:
        md = f.read()
    html_content = cmarkgfm.github_flavored_markdown_to_html(md, options=(
                                            cmarkgfmOptions.CMARK_OPT_GITHUB_PRE_LANG
                                            | cmarkgfmOptions.CMARK_OPT_SMART
                                            | cmarkgfmOptions.CMARK_OPT_HARDBREAKS
                                            | cmarkgfmOptions.CMARK_OPT_VALIDATE_UTF8
                                    ))
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Webhook Feeds",
        swagger_favicon_url=".assets/favicon.ico"
    )


@app.get("/feeds/", response_model=list[FeedPublic], tags=["feeds"], summary="Get all feeds")
async def get_feeds(
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
    feeds = session.exec(select(Feed).offset(offset).limit(limit)).all()
    return feeds


@app.get("/feeds/{feed_id}", response_model=FeedPublic, tags=["feeds"], summary="Get feed")
async def get_feed(feed_id: uuid.UUID, session: Session = Depends(get_session)):
    feed = session.get(Feed, feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="feed not found")
    return feed


@app.post("/feeds/", response_model=FeedPublic, tags=["feeds"], summary="Create feed")
async def add_feed(feed: FeedBase, session: Session = Depends(get_session)):
    feed_db = Feed.model_validate(feed)
    session.add(feed_db)
    session.commit()
    session.refresh(feed_db)
    return feed_db


@app.patch("/feeds/{feed_id}", response_model=FeedPublic, tags=["feeds"], summary="Update feed")
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


@app.delete("/feeds/{feed_id}", tags=["feeds"], summary="Delete feed")
def delete_feed(feed_id: uuid.UUID, session: Session = Depends(get_session)):
    feed_db = session.get(Feed, feed_id)
    if not feed_db:
        raise HTTPException(status_code=404, detail="feed not found")
    session.delete(feed_db)
    session.commit()
    return {"ok": True}


@app.get("/feeds/{feed_id}/feeditems/", response_model=list[FeedItemPublic], tags=["feed items"],
         summary="Get feed items for a feed")
async def get_feeditems(feed_id: uuid.UUID, session: Session = Depends(get_session), offset: int = 0,
                        limit: Annotated[int, Query(le=100)] = 100):
    feed = session.get(Feed, feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="feed not found")
    feeditems = session.exec(select(FeedItem).where(FeedItem.feed_id == feed_id).offset(offset).limit(limit)).all()
    return feeditems


@app.get("/feeds/{feed_id}/feeditems/{feeditem_id}", response_model=FeedItemPublic, tags=["feed items"],
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


@app.post("/feeds/{feed_id}/feeditems/", response_model=FeedItemPublic, tags=["feed items"], summary="Create feed item")
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


async def create_feeditem(feed_id, feeditem, session):
    extra_data = {"feed_id": feed_id}
    feeditem = feeditem
    feeditem_db = FeedItem.model_validate(feeditem, update=extra_data)
    session.add(feeditem_db)
    session.commit()
    session.refresh(feeditem_db)
    return feeditem_db


@app.patch("/feeds/{feed_id}/feeditems/{feeditem_id}", response_model=FeedItemPublic, tags=["feed items"],
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


async def update_feeditem(feeditem, feeditem_db, session):
    feeditem_data = feeditem.model_dump(exclude_unset=True)
    feeditem_db.sqlmodel_update(feeditem_data)
    session.add(feeditem_db)
    session.commit()
    session.refresh(feeditem_db)
    return feeditem_db


@app.delete("/feeds/{feed_id}/feeditems/{feeditem_id}", tags=["feed items"], summary="Delete feed item")
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


@app.get("/feeds/{feed_id}/rssfeed/", response_class=Response, tags=["feed renderer"], summary="Get RSS feed")
def get_rssfeed(feed_id: uuid.UUID, session: Session = Depends(get_session)):
    feed = session.get(Feed, feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="feed not found")
    data: str = generate_feed(feed_id, session)
    return Response(content=data, media_type="application/xml")


@app.get("/feeds/{feed_id}/atomfeed/", response_class=Response, tags=["feed renderer"], summary="Get Atom feed")
def get_atomfeed(feed_id: uuid.UUID, session: Session = Depends(get_session)):
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
