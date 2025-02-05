import datetime

from sqlmodel import Session
from starlette.testclient import TestClient

from app.models.diun import DiunNotification, get_title, get_description
from app.models.feed import Feed


async def test_add_feeditem(session: Session, client: TestClient):
    feed = Feed(title="My Feed", link="https://feed.com/")
    session.add(feed)
    session.commit()

    metadata: dict = {"key1": "value1"}

    diun_notif: DiunNotification = DiunNotification(diun_version="v4.29.0",
                                                    hostname="diun_turrican",
                                                    status="new",
                                                    provider="file",
                                                    image="docker.io/diun/testnotif:latest",
                                                    hub_link="",
                                                    mime_type="application/vnd.docker.distribution.manifest.list.v2+json",
                                                    digest="sha256:216e3ae7de4ca8b553eb11ef7abda00651e79e537e85c46108284e5e91673e01",
                                                    created=datetime.datetime.now(),
                                                    platform="linux/amd64",
                                                    metadata=metadata)

    response = client.post(
        "/feeds/" + str(feed.id) + "/diun/", content=diun_notif.model_dump_json())

    data = response.json()

    assert response.status_code == 200
    assert data["title"] == await get_title(diun_notif)
    assert data["link"] == ""
    assert data["description"] == await get_description(diun_notif)
    assert data["pubDate"] is not None
    assert data["guid"] == diun_notif.digest
