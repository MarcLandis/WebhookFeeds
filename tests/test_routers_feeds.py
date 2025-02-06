from sqlmodel import Session
from starlette.testclient import TestClient

from app.models.feed import Feed


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
        json={
            "title": "My Feed",
            "link": "https://feed.com/",
            "pubDate": "2025-02-04T13:57:24.722Z",
        },
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
