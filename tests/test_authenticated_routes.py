def test_dashboard_user_logged_in(client):
    with client.session_transaction() as sess:
        sess['username'] = 'testuser'
        sess['role'] = 'User'
    response = client.get('/dashboard_user')
    assert response.status_code == 200
    assert b"User Dashboard" in response.data  # Example check

def test_submit_ticket_logged_in(client):
    with client.session_transaction() as sess:
        sess['username'] = 'testuser'
        sess['role'] = 'User'
    response = client.get('/submit_ticket')
    assert response.status_code == 200
    assert b"Submit Ticket" in response.data

def test_dashboard_admin_logged_in(client):
    with client.session_transaction() as sess:
        sess['username'] = 'adminuser'
        sess['role'] = 'Admin'
    response = client.get('/dashboard_admin')
    assert response.status_code == 200
    assert b"Admin Dashboard" in response.data

def test_dashboard_it_logged_in(client):
    with client.session_transaction() as sess:
        sess['username'] = 'itsupport'
        sess['role'] = 'IT Support'
    response = client.get('/dashboard_it')
    assert response.status_code == 200
    assert b"IT Staff Dashboard" in response.data
