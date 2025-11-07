
def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data

def test_logout_redirect(client):
    response = client.get("/logout")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_register_page(client):
    response = client.get("/register")
    assert response.status_code == 200
