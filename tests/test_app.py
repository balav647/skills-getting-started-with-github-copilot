import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Use a unique email for testing
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"

    # Ensure not already registered
    client.post(f"/activities/{activity}/unregister?email={test_email}")

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json()["message"]

    # Check participant is in list
    activities = client.get("/activities").json()
    assert test_email in activities[activity]["participants"]

    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert response.status_code == 200
    assert f"Unregistered {test_email}" in response.json()["message"]

    # Check participant is removed
    activities = client.get("/activities").json()
    assert test_email not in activities[activity]["participants"]
