
import pytest
from app import app as flask_app, mysql

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "MYSQL_DB": "helpdesk_test_db"
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_data_once():
    # yield so this runs AFTER all tests in the session
    yield
    # ensure we have an app context for DB operations
    with flask_app.app_context():
        cur = mysql.connection.cursor()
        try:
            cur.execute("DELETE FROM tickets WHERE title LIKE 'Test%'")
            cur.execute("DELETE FROM users WHERE username LIKE 'pytest_%'")
            mysql.connection.commit()
        finally:
            cur.close()