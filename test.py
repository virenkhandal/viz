import requests
import pdb
from analysis import analyze
import time

def get_spotify_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

def search_track(title, access_token):
    search_url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    params = {
        'q': title,
        'type': 'track',
        'limit': 1  # Assuming you want the first matching result
    }
    response = requests.get(search_url, headers=headers, params=params)
    return response.json()

# Your Spotify App Credentials
client_id = '61bb4c3ea3c24253a738bd8f34956191'
client_secret = '43e1501fc8d94c768d8af79f096395eb'

access_token = get_spotify_access_token(client_id, client_secret)
track_title = "Shape of You"  # Example track title
track_info = search_track(track_title, access_token)

def get_analysis(track_id):
    search_url = f'https://api.spotify.com/v1/audio-analysis/{track_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(search_url, headers=headers)
    return response.json()

if track_info['tracks']['items']:
    start = time.time()
    first_track_id = track_info['tracks']['items'][0]['id']
    print(f"Track ID: {first_track_id}")
    track_info = get_analysis(first_track_id)
    analyze(track_info)
    end = time.time()
    # print(f"Latency for request from song title to analysis: {round(end - start, 4)} seconds...")

else:
    print("No track found")
