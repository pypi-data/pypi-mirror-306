import requests
import webbrowser
from tqdm import tqdm

BASE_URL = "https://flask-app-749005010020.us-central1.run.app"

session = requests.Session()

def start_auth():
    """Start authentication by prompting the user to log in."""
    # Request the login URL from the Flask app
    response = session.get(BASE_URL)
    
    if response.status_code == 200:
        # Extract the login URL from the response
        auth_url = response.text.split('href="')[1].split('"')[0]
        print(f"Please go to this URL and authorize access: {auth_url}")
        webbrowser.open(auth_url)   
        # Wait for the user to confirm that they've completed authentication
        session_id = input("After completing the login, please enter your session ID from the browser window: ")
        session.cookies.set('session', session_id)  

def is_authenticated():
    """Check if the user is authenticated."""
    response = session.get(f"{BASE_URL}/is-authenticated")
    if response.status_code == 200:
        data = response.json()
        return data.get("authenticated", False)
    else:
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("Error: Received non-JSON response.")
        print("Response text:", response.text)
        return False

def find_duplicates():
    """Finds duplicate tracks using the authenticated user's session."""
    if not is_authenticated():
        print("User not authenticated. Please authenticate first.")
        return
    
    response = session.get(f"{BASE_URL}/find-duplicates")
    
    if response.status_code == 200:
        data = response.json()
        if "duplicates" in data:
            duplicates = data["duplicates"]
            if duplicates:
                print("\nFound duplicates:")
                for dup in duplicates:
                    print(f"- {dup}")
                return data.get("session_id")
        else:
            print("No duplicates found.")
            return None
    else:
        print("Error finding duplicates:", response.json())

def delete_duplicates(session_id):
    """Deletes duplicate tracks using the given session ID."""
    if not session_id:
        return
    
    response = session.post(
        f"{BASE_URL}/delete-duplicates",
        json={"session_id": session_id}
    )
    
    if response.status_code == 200:
        print("Duplicates deleted successfully.")
    else:
        print("Error deleting duplicates:", response.json())

def main():
    """Main entry point for the CLI app."""
    # Start authentication and wait for the user to log in
    if not is_authenticated():
        start_auth()  
    
    action = input("Welcome to the Spotify management tool. Enter an action (duplicate): ").strip().lower()
    
    if action == "duplicate":
        session_id = find_duplicates()
        if session_id:
            delete = input("Do you want to delete the duplicates? (Yes/No): ").strip().lower()
            if delete == "yes":
                delete_duplicates(session_id)
    else:
        print("Invalid action.")

if __name__ == "__main__":
    main()
