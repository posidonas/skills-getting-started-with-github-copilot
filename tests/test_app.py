import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_list_activities():
    # Arrange: (No setup needed for in-memory activities)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("description" in v for v in data.values())

def test_signup_success():
    # Arrange
    email = "student1@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Clean up: Remove participant if DELETE is implemented

@pytest.mark.parametrize("email", ["student2@mergington.edu"])
def test_signup_duplicate(email):
    # Arrange
    activity = next(iter(client.get("/activities").json().keys()))
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400 or response.status_code == 409
    assert "already registered" in response.json().get("detail", "")

def test_signup_nonexistent_activity():
    # Arrange
    email = "student3@mergington.edu"
    activity = "nonexistent-activity"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")
