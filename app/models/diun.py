import uuid
from datetime import datetime
from typing import Union, Any

from fastapi import Depends
from pydantic import BaseModel, Field
from sqlmodel import Session

from app.dependencies import get_session
from app.models.feeditem import FeedItemBase
from app.routers.feeditems import add_feeditem


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
    metadata: Union[Any, None] = Field(default=None)


async def get_title(notif: DiunNotification) -> str:
    return f"Docker tag {notif.image} updated (triggered by {notif.hostname})"


async def get_description(notif: DiunNotification) -> str:
    return f"Docker tag <a href=\"{notif.hub_link}\">{notif.image}</a> updated (triggered by {notif.hostname})"


async def create_feeditem(feed_id: uuid.UUID, notif: DiunNotification,
                          session: Session = Depends(get_session)) -> FeedItemBase:
    title = await get_title(notif)
    description = await get_description(notif)

    feeditembase: FeedItemBase = FeedItemBase(
        title=title,
        link=notif.hub_link,
        description=description,
        guid=notif.digest,
        pubDate=notif.created
    )

    feeditem = await add_feeditem(feed_id, feeditembase, session)
    return feeditem
