def test_register_and_login(client):
    r = client.post("/auth/register", json={"email": "a@b.com", "password": "secret123"})
    assert r.status_code == 201
    r = client.post("/auth/login", json={"email": "a@b.com", "password": "secret123"})
    assert r.status_code == 200 and "access_token" in r.json()
