import uuid
from datetime import datetime
from typing import Union

from sqlmodel import Field, SQLModel


class FeedBase(SQLModel):
    title: str = Field(title="feed title")
    link: str = Field(title="feed link")
    description: Union[str, None] = Field(default=None, title="feed description")
    pubDate: Union[datetime, None] = Field(
        default=None, index=True, title="feed publication date"
    )


class Feed(FeedBase, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, title="unique feed id"
    )


class FeedPublic(FeedBase):
    id: Union[uuid.UUID, None] = Field(default=None, title="unique feed id")


class FeedUpdate(FeedBase):
    title: Union[str, None] = Field(default=None, title="feed title")
    link: Union[str, None] = Field(default=None, title="feed link")
    description: Union[str, None] = Field(default=None, title="feed description")
    pubDate: Union[datetime, None] = Field(default=None, title="feed publication date")
