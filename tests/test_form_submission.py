import pytest

def test_register_user(client):
    username = "pytest_user"
    response = client.post("/register", data={
        "username": username,
        "password": "pytest_pass",
        "role": "User"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Registration successful" in response.data or b"Login" in response.data

@pytest.mark.dependency(depends=["test_register_user"])
def test_login_valid(client):
    response = client.post("/login", data={
        "username": "pytest_user",
        "password": "pytest_pass"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Dashboard" in response.data

def test_submit_ticket(client):
    with client.session_transaction() as sess:
        sess["username"] = "pytest_user"
        sess["role"] = "User"

    response = client.post("/submit_ticket", data={
        "title": "Test Ticket",
        "description": "This is a test ticket.",
        "category": "Software",
        "priority": "High"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Ticket submitted successfully" in response.data
