from fastapi.testclient import TestClient

import cft_internship
from cft_internship.main import app

client = TestClient(cft_internship.main.app)


def test_data_without_auth():
    response = client.get("/data")
    assert response.status_code == 401


def login():
    response = client.post("/login", data={"username": "soramiyazaki", "password": "123"},
                           headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
