import uuid
from datetime import datetime
from typing import Union

from sqlmodel import Field, SQLModel


class FeedItemBase(SQLModel):
    title: str = Field(title="feed item title")
    link: str = Field(title="feed item link")
    description: Union[str, None] = Field(default=None, title="feed item description")
    pubDate: Union[datetime, None] = Field(default=None, index=True, title="feed item publication date")
    guid: Union[str, None] = Field(default=None, title="feed item guid")


class FeedItem(FeedItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, title="unique feed item id")
    feed_id: uuid.UUID = Field(index=True, foreign_key="feed.id", ondelete="CASCADE",
                               title="feed id to add the item to")


class FeedItemPublic(FeedItemBase):
    id: Union[uuid.UUID, None] = Field(default=None, title="unique feed item id")
    feed_id: Union[uuid.UUID, None] = Field(default=None, title="feed id to add the item to")


class FeedItemUpdate(FeedItemBase):
    title: Union[str, None] = Field(default=None, title="feed title")
    link: Union[str, None] = Field(default=None, title="feed link")
    description: Union[str, None] = Field(default=None, title="feed description")
    guid: Union[str, None] = Field(default=None, title="feed item guid")
