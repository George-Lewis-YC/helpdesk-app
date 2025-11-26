import pytest
from app import app as flask_app
import pymysql

@pytest.fixture
def test_app():
    flask_app.config.update({
        "TESTING": True,
        "MYSQL_DB": "helpdesk_test_db"
    })
    yield flask_app

@pytest.fixture
def client(test_app):
    return test_app.test_client()

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_data_once():
    yield
    # Cleanup after all tests
    conn = pymysql.connect(host="localhost", user="root", password="admin", db="helpdesk_test_db")
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tickets WHERE title LIKE 'Test%'")
            cur.execute("DELETE FROM users WHERE username LIKE 'pytest_%'")
        conn.commit()
    finally:
        conn.close()
