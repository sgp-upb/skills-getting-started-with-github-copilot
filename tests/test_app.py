def test_get_activities_returns_activities(client):
    # Arrange
    expected_keys = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert expected_keys.issubset(set(data.keys()))


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={new_email}")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == f"Signed up {new_email} for {activity_name}"

    response = client.get("/activities")
    assert new_email in response.json()[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Programming Class"
    duplicate_email = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={duplicate_email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant_unregisters_participant(client):
    # Arrange
    activity_name = "Gym Class"
    email_to_remove = "john@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email_to_remove}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email_to_remove} from {activity_name}"

    response = client.get("/activities")
    assert email_to_remove not in response.json()[activity_name]["participants"]


def test_remove_participant_not_found_returns_404(client):
    # Arrange
    activity_name = "Gym Class"
    missing_email = "missingstudent@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={missing_email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
