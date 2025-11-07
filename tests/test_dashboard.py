
def test_user_dashboard_redirect(client):
    response = client.get("/dashboard_user")
    assert response.status_code == 302

def test_admin_dashboard_redirect(client):
    response = client.get("/dashboard_admin")
    assert response.status_code == 302

def test_it_dashboard_redirect(client):
    response = client.get("/dashboard_it")
    assert response.status_code == 302
