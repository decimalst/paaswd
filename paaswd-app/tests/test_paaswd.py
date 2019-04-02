import os
import tempfile

import pytest
from paaswd import create_app
from paaswd.db import get_db, init_db

# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # create the database and load test data
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_empty_db(client):
    """Test if / gives us back the response that the app is alive."""
    rv = client.get('/')
    assert b'alive' in rv.data

def test_get_user(client):
    """Test if our user query endpoint works"""
    rv = client.get('/api/users/0')
    assert b'root' in rv.data

def test_get_user_negative(client):
    """Test if we don't get anything back when we ask for a user that doesn't exist"""
    rv = client.get('/api/users/22')
    assert b'root' not in rv.data

def test_get_group(client):
    """Test if we don't get anything back when we ask for a user that doesn't exist"""
    rv = client.get('/api/groups/22')
    assert b'root' not in rv.data

def test_get_all_users(client):
    """Tests for good/bad data in all users response"""
    rv = client.get('/api/users')
    assert b'quack' not in rv.data
    assert b'root' in rv.data

def test_get_all_users_query(client):
    """Tests for good/bad data in all users response"""
    rv = client.get('/api/users/query?name=root')
    assert b'ubuntu' not in rv.data
    assert b'root' in rv.data

def test_get_user_groups(client):
    """Tests for good/bad data in all users response"""
    rv = client.get('/api/users/1001/groups')
    assert b'root' not in rv.data
    assert b'sudo' in rv.data

def test_get_all_groups(client):
    """Tests for good/bad data in all users response"""
    rv = client.get('/api/groups')
    assert b'root' in rv.data
    assert b'sudo' in rv.data

def test_get_group_by_id(client):
    """Tests for good/bad data in all users response"""
    rv = client.get('/api/groups/1001')
    assert b'root' not in rv.data
    assert b'sudo' in rv.data
    
def test_get_group_by_query(client):
    """Tests for good/bad data in all users response"""
    rv = client.get('/api/groups/query?member=root')
    assert b'root' in rv.data
    assert b'sudo' not in rv.data