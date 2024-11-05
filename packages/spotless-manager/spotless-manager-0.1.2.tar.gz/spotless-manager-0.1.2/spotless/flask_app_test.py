import pytest
from flask import session
from .app import app, sessions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection in testing mode
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_index_redirects_to_auth_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Sign in' in response.data  # Check if the response contains "Sign in" link

def test_is_authenticated_when_not_authenticated(client):
    response = client.get('/is-authenticated')
    assert response.status_code == 401
    assert response.get_json() == {"authenticated": False}

def test_find_duplicates_redirects_when_not_authenticated(client):
    response = client.get('/find-duplicates')
    assert response.status_code == 302  # Redirect to authentication page

def test_delete_duplicates_fails_without_session_id(client):
    response = client.post('/delete-duplicates', json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid or expired session ID"}

def test_delete_duplicates_fails_with_invalid_session_id(client):
    response = client.post('/delete-duplicates', json={"session_id": "invalid_session_id"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid or expired session ID"}

def test_find_duplicates_no_duplicates_found(client, mocker):
    """Tests the case where no duplicates are found."""
    # Mock Spotify responses to return no duplicates
    mock_spotify = mocker.patch("app.spotify.current_user_saved_tracks", return_value={
        "items": [],
        "next": None
    })
    
    mock_oauth = mocker.patch("app.spotipy.oauth2.SpotifyOAuth.validate_token", return_value=True)

    response = client.get('/find-duplicates')
    assert response.status_code == 200
    assert response.get_json() == {"message": "No duplicates found!"}

def test_delete_duplicates_success(client, mocker):
    """Tests successful deletion of duplicates."""
    # Setup a session ID and mock Spotify delete function
    session_id = "test-session-id"
    sessions[session_id] = {"track_ids": ["track1", "track2", "track3"]}

    mocker.patch("app.spotipy.oauth2.SpotifyOAuth.validate_token", return_value=True)
    mock_spotify = mocker.patch("app.spotify.current_user_saved_tracks_delete")

    response = client.post('/delete-duplicates', json={"session_id": session_id})
    assert response.status_code == 200
    assert response.get_json() == {"message": "All done! Duplicates deleted"}
    assert session_id not in sessions  # Ensure session is removed after deletion

