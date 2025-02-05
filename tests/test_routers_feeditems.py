from sqlmodel import Session
from starlette.testclient import TestClient

from app.models.feed import Feed
from app.models.feeditem import FeedItem


def test_get_feeditems(session: Session, client: TestClient):
    feed = Feed(title="My Feed", link="https://feed.com/")
    session.add(feed)
    session.commit()

    feeditem_1 = FeedItem(title="My Feed Item 1", link="https://feeditem1.com/", feed_id=feed.id)
    feeditem_2 = FeedItem(title="My Feed Item 2", link="https://feeditem2.com/", feed_id=feed.id)
    session.add(feeditem_1)
    session.add(feeditem_2)
    session.commit()

    response = client.get("/feeds/" + str(feed.id) + "/feeditems/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["title"] == feeditem_1.title
    assert data[0]["link"] == feeditem_1.link
    assert data[0]["description"] is None
    assert data[0]["id"] == str(feeditem_1.id)
    assert data[1]["title"] == feeditem_2.title
    assert data[1]["link"] == feeditem_2.link
    assert data[1]["description"] is None
    assert data[1]["id"] == str(feeditem_2.id)


def test_get_feeditems_by_feed_id(session: Session, client: TestClient):
    feed = Feed(title="My Feed", link="https://feed.com/")
    session.add(feed)
    session.commit()

    feeditem_1 = FeedItem(title="My Feed Item 1", link="https://feeditem1.com/", feed_id=feed.id)
    feeditem_2 = FeedItem(title="My Feed Item 2", link="https://feeditem2.com/", feed_id=feed.id)
    session.add(feeditem_1)
    session.add(feeditem_2)
    session.commit()

    response = client.get("/feeds/" + str(feed.id) + "/feeditems/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["title"] == feeditem_1.title
    assert data[0]["link"] == feeditem_1.link
    assert data[0]["description"] is None
    assert data[0]["id"] == str(feeditem_1.id)
    assert data[1]["title"] == feeditem_2.title
    assert data[1]["link"] == feeditem_2.link
    assert data[1]["description"] is None
    assert data[1]["id"] == str(feeditem_2.id)


def test_add_feeditem(session: Session, client: TestClient):
    feed = Feed(title="My Feed", link="https://feed.com/")
    session.add(feed)
    session.commit()

    response = client.post(
        "/feeds/" + str(feed.id) + "/feeditems/?insert_or_update=True",
        json={"title": "My Feed Item", "link": "https://feeditem.com/", "pubDate": "2025-02-04T13:57:24.722Z",
              "guid": "123456"}
    )

    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "My Feed Item"
    assert data["link"] == "https://feeditem.com/"
    assert data["description"] is None
    assert data["pubDate"] is not None
    assert data["guid"] == "123456"


def test_add_feeditem_update(session: Session, client: TestClient):
    feed = Feed(title="My Feed", link="https://feed.com/")
    session.add(feed)
    session.commit()

    client.post(
        "/feeds/" + str(feed.id) + "/feeditems/?insert_or_update=True",
        json={"title": "My Feed Item", "link": "https://feeditem.com/", "pubDate": "2025-02-04T13:57:24.722Z",
              "guid": "123456"}
    )

    response = client.post(
        "/feeds/" + str(feed.id) + "/feeditems/?insert_or_update=True",
        json={"title": "My Feed Item Updated", "link": "https://feeditem.com/", "pubDate": "2025-02-05T13:57:24.722Z",
              "guid": "123456"}
    )

    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "My Feed Item Updated"
    assert data["link"] == "https://feeditem.com/"
    assert data["description"] is None
    assert data["pubDate"] is not None
    assert data["guid"] == "123456"


def test_add_feeditem_no_update(session: Session, client: TestClient):
    feed = Feed(title="My Feed", link="https://feed.com/")
    session.add(feed)
    session.commit()

    client.post(
        "/feeds/" + str(feed.id) + "/feeditems/?insert_or_update=False",
        json={"title": "My Feed Item", "link": "https://feeditem.com/", "pubDate": "2025-02-04T13:57:24.722Z",
              "guid": "123456"}
    )

    response = client.post(
        "/feeds/" + str(feed.id) + "/feeditems/?insert_or_update=False",
        json={"title": "My Feed Item Updated", "link": "https://feeditem.com/", "pubDate": "2025-02-05T13:57:24.722Z",
              "guid": "123456"}
    )

    data = response.json()

    assert response.status_code == 409
    assert data["detail"] == "feed item already exists"


def test_update_feeditem(session: Session, client: TestClient):
    feed = Feed(title="My Feed", link="https://feed.com/")
    session.add(feed)
    session.commit()

    feeditem = FeedItem(title="My Feed Item", link="https://feeditem.com/", feed_id=feed.id)
    session.add(feeditem)
    session.commit()

    feeditem_update = {"title": "My Feed Item Updated", "link": "https://feeditem.com/"}

    response = client.patch("/feeds/" + str(feed.id) + "/feeditems/" + str(feeditem.id), json=feeditem_update)
    data = response.json()

    assert response.status_code == 200

    assert data["title"] != "My Feed Item"
    assert data["title"] == "My Feed Item Updated"
    assert data["link"] == feeditem.link
    assert data["link"] == "https://feeditem.com/"
    assert data["description"] is None
    assert data["id"] == str(feeditem.id)


def test_delete_feeditem(session: Session, client: TestClient):
    feed = Feed(title="My Feed", link="https://feed.com/")
    session.add(feed)
    session.commit()

    feeditem = FeedItem(title="My Feed Item", link="https://feeditem.com/", feed_id=feed.id)
    session.add(feeditem)
    session.commit()

    response = client.delete("/feeds/" + str(feed.id) + "/feeditems/" + str(feeditem.id))
    data = response.json()

    assert response.status_code == 200
    assert data == {"ok": True}
