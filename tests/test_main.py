from sqlmodel import Session
from starlette.testclient import TestClient

from app.models import Feed, FeedItem


def test_root(session: Session, client: TestClient):
    response = client.get("/")
    assert response.status_code == 200


def test_license(session: Session, client: TestClient):
    response = client.get("/LICENSE.md")
    assert response.status_code == 200


def test_docs(session: Session, client: TestClient):
    response = client.get("/docs")
    assert response.status_code == 200


def test_get_feeds(session: Session, client: TestClient):
    feed_1 = Feed(title="My Feed 1", link="https://feed1.com/")
    feed_2 = Feed(title="My Feed 2", link="https://feed2.com/")
    session.add(feed_1)
    session.add(feed_2)
    session.commit()

    response = client.get("/feeds/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["title"] == feed_1.title
    assert data[0]["link"] == feed_1.link
    assert data[0]["description"] is None
    assert data[0]["id"] == str(feed_1.id)
    assert data[1]["title"] == feed_2.title
    assert data[1]["link"] == feed_2.link
    assert data[1]["description"] is None
    assert data[1]["id"] == str(feed_2.id)


def test_get_feed(session: Session, client: TestClient):
    feed = Feed(title="My Feed", link="https://feed.com/")
    session.add(feed)
    session.commit()

    response = client.get("/feeds/" + str(feed.id))
    data = response.json()

    assert response.status_code == 200

    assert data["title"] == feed.title
    assert data["link"] == feed.link
    assert data["description"] is None
    assert data["id"] == str(feed.id)


def test_add_feed(client: TestClient):
    response = client.post(
        "/feeds/",
        json={"title": "My Feed", "link": "https://feed.com/", "pubDate": "2025-02-04T13:57:24.722Z"}
    )

    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "My Feed"
    assert data["link"] == "https://feed.com/"
    assert data["description"] is None
    assert data["pubDate"] is not None


def test_update_feed(session: Session, client: TestClient):
    feed = Feed(title="My Feed", link="https://feed.com/")
    session.add(feed)
    session.commit()

    feed_update = {"title": "My Feed Updated", "link": "https://feed.com/"}

    response = client.patch("/feeds/" + str(feed.id), json=feed_update)
    data = response.json()

    assert response.status_code == 200

    assert data["title"] != "My Feed"
    assert data["title"] == "My Feed Updated"
    assert data["link"] == feed.link
    assert data["link"] == "https://feed.com/"
    assert data["description"] is None
    assert data["id"] == str(feed.id)


def test_delete_feed(session: Session, client: TestClient):
    feed = Feed(title="My Feed", link="https://feed.com/")
    session.add(feed)
    session.commit()

    response = client.delete("/feeds/" + str(feed.id))
    data = response.json()

    assert response.status_code == 200
    assert data == {"ok": True}


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


def test_get_rssfeed(session: Session, client: TestClient):
    feed = Feed(title="My Feed", link="https://feed.com/")
    session.add(feed)
    session.commit()

    feeditem_1 = FeedItem(title="My Feed Item 1", link="https://feeditem1.com/", feed_id=feed.id)
    feeditem_2 = FeedItem(title="My Feed Item 2", link="https://feeditem2.com/", feed_id=feed.id)
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

    feeditem_1 = FeedItem(title="My Feed Item 1", link="https://feeditem1.com/", feed_id=feed.id)
    feeditem_2 = FeedItem(title="My Feed Item 2", link="https://feeditem2.com/", feed_id=feed.id)
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
