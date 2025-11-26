def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"<form" in response.data  # Check for form instead of text

def test_logout_redirect(client):
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers.get("Location", "")

def test_register_page(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"<form" in response.data
