from starlette.testclient import TestClient


def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200


def test_license(client: TestClient):
    response = client.get("/LICENSE.md")
    assert response.status_code == 200


def test_docs(client: TestClient):
    response = client.get("/docs")
    assert response.status_code == 200
