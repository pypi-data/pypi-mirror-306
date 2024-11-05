from flask import Flask, request, jsonify, session, redirect, make_response
from flask_session import Session
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from collections import defaultdict
import uuid
import os

# Flask app initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'notsecretkey123'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['SESSION_TYPE'] = 'filesystem'
session_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.flask_session')
if not os.path.exists(session_dir):
    os.makedirs(session_dir, exist_ok=True)
app.config['SESSION_FILE_DIR'] = session_dir
app.config['SESSION_PERMANENT'] = True
Session(app)

# In-memory dictionary to store session data
sessions = {}

# Define the required Spotify API scope
scope = "user-library-read user-library-modify"

# Spotify client setup
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(),
    auth_manager=SpotifyOAuth(scope=scope),
)

def dup_search(results, seen, dupes):
    for item in results["items"]:
        track = item["track"]
        track_name = track["name"]
        cur_artist_names = {artist["name"] for artist in track["artists"]}
        if track_name in seen:
            if seen[track_name] == cur_artist_names:
                dupes[track_name].append(track)
        else:
            seen[track_name] = cur_artist_names
            
@app.route('/')
def index():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-library-read user-library-modify',
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    if request.args.get("code"):
        #Being redirected from Spotify auth page with a code
        token_info = auth_manager.get_access_token(request.args.get("code"))

        # Save the token to the session explicitly
        cache_handler.save_token_to_cache(token_info)
        response = make_response(f'<h2>Authentication successful! Enter the following session id in the terminal where you ran spotless. Your session ID is: {session.sid}</h2>')
        return response

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'

        
@app.route('/is-authenticated', methods=['GET'])
def is_authenticated():
    """Check if the user is authenticated and provide their status."""
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)

    token_info = cache_handler.get_cached_token()

    if token_info and auth_manager.validate_token(token_info):
        print("Token is valid.")
        return jsonify({"authenticated": True}), 200
    else:
        print("Token is not valid or missing.")
        return jsonify({"authenticated": False}), 401
    
@app.route('/find-duplicates', methods=['GET'])
def find_duplicates():
    """Finds and returns duplicate tracks and generates a session ID."""
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    seen = defaultdict(set)
    dupes = defaultdict(list)
    all_tracks = spotify.current_user_saved_tracks(limit=50)
    dup_search(all_tracks, seen, dupes)
        # Process subsequent pages
    while all_tracks["next"]:
        all_tracks = spotify.next(all_tracks)
        dup_search(all_tracks, seen, dupes)
    if len(dupes) == 0:
        return jsonify({"message": "No duplicates found!"})
    
    # Generate a unique session ID
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "track_ids": [dup["id"] for tracks in dupes.values() for dup in tracks]
    }

    return jsonify({
        "message": "Duplicates found!",
        "session_id": session_id,
        "duplicates": list(dupes.keys())
    })

@app.route('/delete-duplicates', methods=['POST'])
def delete_duplicates():
    """Deletes duplicate tracks based on the provided session ID."""
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    data = request.json
    session_id = data.get("session_id")
    
    if not session_id or session_id not in sessions:
        return jsonify({"error": "Invalid or expired session ID"}), 400

    # Retrieve the track IDs for this session
    track_ids = sessions[session_id]["track_ids"]
    
    # Can delete a max of 50 tracks at a time
    for i in range(0, len(track_ids), 50):
        spotify.current_user_saved_tracks_delete(tracks=track_ids[i: i + 50])

    # Clean up the session after use
    del sessions[session_id]

    return jsonify({"message": "All done! Duplicates deleted"}), 200

# Main entry point for running the app locally
if __name__ == '__main__':
    app.run(threaded=True, port=int(os.environ.get("PORT", os.environ.get("SPOTIPY_REDIRECT_URI", 8888).split(":")[-1])))