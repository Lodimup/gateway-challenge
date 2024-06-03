"""
Test Auth endpoints
"""

import httpx

from services.env_man import ENVS

base_url = "http://localhost:8000"
if ENVS.get("DEPLOYENV") == "test":
    base_url = "http://nginx:80"

client = httpx.Client(base_url=base_url)


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
