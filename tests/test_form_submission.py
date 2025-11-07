
import pytest
from flask import session

# Test user registration form submission
def test_register_user(client):
    response = client.post("/register", data={
        "username": "pytest_user",
        "password": "pytest_pass",
        "role": "User"
    }, follow_redirects=True)
    assert b"Registration successful" in response.data

# Test login with valid credentials
def test_login_valid(client):
    response = client.post("/login", data={
        "username": "pytest_user",
        "password": "pytest_pass"
    }, follow_redirects=True)
    assert b"Dashboard" in response.data

# Test ticket submission form
def test_submit_ticket(client, app):
    with app.test_request_context():
        with client.session_transaction() as sess:
            sess["username"] = "pytest_user"
            sess["role"] = "User"

        response = client.post("/submit_ticket", data={
            "title": "Test Ticket",
            "description": "This is a test ticket.",
            "category": "Software",
            "priority": "High"
        }, follow_redirects=True)
        assert b"Ticket submitted successfully" in response.data
