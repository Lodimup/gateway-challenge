import httpx

client = httpx.Client(base_url="http://localhost:8000")


def test_auth_success():
    r_auth = client.post(
        "/auth/token",
        data={
            "username": "johndoe",
            "password": "secret",
        },
    )

    assert r_auth.status_code == 200
    assert r_auth.json() == {"access_token": "johndoe", "token_type": "bearer"}

    headers = {"Authorization": f"Bearer {r_auth.json()['access_token']}"}
    r_me = client.get("user/me", headers=headers)
    assert r_me.status_code == 200


def test_auth_fail():
    r = client.post(
        "/auth/token",
        data={
            "username": "johndoe",
            "password": "wrong",
        },
    )
    assert r.status_code == 400
    assert r.json() == {"detail": "Incorrect username or password"}
