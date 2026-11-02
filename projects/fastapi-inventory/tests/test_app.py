from fastapi.testclient import TestClient
from main import app
client=TestClient(app)
def test_health():
    assert client.get("/health").json()=={"status":"ok"}
def test_validate_quantity():
    assert client.post("/items/5",json={"name":"Mouse","quantity":-3}).status_code==422
def test_create_and_list():
    assert client.post("/items/5",json={"name":"Mouse","quantity":3}).status_code==200
    assert any(x["id"]==5 for x in client.get("/items").json())
