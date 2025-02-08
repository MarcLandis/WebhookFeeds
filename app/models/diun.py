import uuid
from datetime import datetime
from typing import Union, Any, Dict

from fastapi import Depends
from pydantic import BaseModel, Field
from sqlmodel import Session

from app.dependencies import get_session
from app.models.feeditem import FeedItemBase
from app.routers.feeditems import add_feeditem
from app.util import get_template


class DiunNotification(BaseModel):
    diun_version: Union[str, None] = Field(default=None)
    hostname: Union[str, None] = Field(default=None)
    status: Union[str, None] = Field(default=None)
    provider: Union[str, None] = Field(default=None)
    image: Union[str, None] = Field(default=None)
    hub_link: Union[str, None] = Field(default=None)
    mime_type: Union[str, None] = Field(default=None)
    digest: Union[str, None] = Field(default=None)
    created: Union[datetime, None] = Field(default=None)
    platform: Union[str, None] = Field(default=None)
    metadata: Union[Dict[str, Any], None] = Field(default=None)


async def get_title(notif: DiunNotification, feed_id: uuid.UUID) -> str:
    template = get_template("title", "diun", feed_id)
    return template.render(notification=notif)


async def get_description(notif: DiunNotification, feed_id: uuid.UUID) -> str:
    template = get_template("description", "diun", feed_id)
    return template.render(notification=notif)


async def create_feeditem(
    feed_id: uuid.UUID, notif: DiunNotification, session: Session = Depends(get_session)
) -> FeedItemBase:
    title = await get_title(notif, feed_id)
    description = await get_description(notif, feed_id)

    feeditembase: FeedItemBase = FeedItemBase(
        title=title,
        link=notif.hub_link,
        description=description,
        guid=notif.digest,
        pubDate=notif.created,
    )

    feeditem = await add_feeditem(feed_id, feeditembase, session)
    return feeditem
