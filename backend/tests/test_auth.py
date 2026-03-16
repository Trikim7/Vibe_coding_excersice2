def test_login_success(client):
    # First register
    client.post("/api/auth/register", json={
        "username": "testuser_login",
        "password": "pass123",
        "full_name": "Test User",
        "role": "librarian"
    })
    resp = client.post("/api/auth/login", data={"username": "testuser_login", "password": "pass123"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "username": "testuser_wrong",
        "password": "correct",
        "full_name": "Test Wrong",
        "role": "librarian"
    })
    resp = client.post("/api/auth/login", data={"username": "testuser_wrong", "password": "wrong"})
    assert resp.status_code == 401


def test_register_duplicate(client):
    data = {"username": "dupuser", "password": "pass", "full_name": "Dup", "role": "librarian"}
    client.post("/api/auth/register", json=data)
    resp = client.post("/api/auth/register", json=data)
    assert resp.status_code == 400
