from sqlmodel import Session
from starlette.testclient import TestClient

from app.models.feed import Feed
from app.models.feeditem import FeedItem


def test_get_rssfeed(session: Session, client: TestClient):
    feed = Feed(title="My Feed", link="https://feed.com/")
    session.add(feed)
    session.commit()

    feeditem_1 = FeedItem(
        title="My Feed Item 1", link="https://feeditem1.com/", feed_id=feed.id
    )
    feeditem_2 = FeedItem(
        title="My Feed Item 2", link="https://feeditem2.com/", feed_id=feed.id
    )
    session.add(feeditem_1)
    session.add(feeditem_2)
    session.commit()

    response = client.get("/feeds/" + str(feed.id) + "/rssfeed/")
    data = response.text

    assert response.status_code == 200

    assert feed.title in data
    assert feeditem_1.title in data
    assert feeditem_2.title in data
    assert feeditem_1.link in data
    assert feeditem_2.link in data


def test_get_atomfeed(session: Session, client: TestClient):
    feed = Feed(title="My Feed", link="https://feed.com/")
    session.add(feed)
    session.commit()

    feeditem_1 = FeedItem(
        title="My Feed Item 1", link="https://feeditem1.com/", feed_id=feed.id
    )
    feeditem_2 = FeedItem(
        title="My Feed Item 2", link="https://feeditem2.com/", feed_id=feed.id
    )
    session.add(feeditem_1)
    session.add(feeditem_2)
    session.commit()

    response = client.get("/feeds/" + str(feed.id) + "/atomfeed/")
    data = response.text

    assert response.status_code == 200

    assert feed.title in data
    assert feeditem_1.title in data
    assert feeditem_2.title in data
    assert feeditem_1.link in data
    assert feeditem_2.link in data
