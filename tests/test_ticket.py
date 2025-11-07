
def test_submit_ticket_redirect(client):
    response = client.get("/submit_ticket")
    assert response.status_code == 302

def test_my_tickets_redirect(client):
    response = client.get("/my_tickets")
    assert response.status_code == 302

def test_ticket_history_redirect(client):
    response = client.get("/my_ticket_history")
    assert response.status_code == 302
