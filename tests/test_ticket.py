def test_submit_ticket_redirect(client):
    response = client.get("/submit_ticket", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers.get("Location", "")

def test_my_tickets_redirect(client):
    response = client.get("/my_tickets", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers.get("Location", "")

def test_ticket_history_redirect(client):
    response = client.get("/my_ticket_history", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers.get("Location", "")
