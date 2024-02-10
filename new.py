import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import threading
import pygame
import requests
import pdb
from analysis import analyze
import time

def initialize_audio(audio_file):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)

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

start = time.time()
first_track_id = track_info['tracks']['items'][0]['id']
print(f"Track ID: {first_track_id}")
track_info = get_analysis(first_track_id)
# analyze(track_info)
# end = time.time()

# Duration of the song in seconds and sample rate for plotting
song_duration = 234  # Example: 5 minutes song
sample_rate = 1  # Update plot every second

# Time and loudness arrays for the plot
times, loudness = analyze(track_info)
# times = np.linspace(0, song_duration, song_duration * sample_rate)
# loudness = np.random.rand(song_duration * sample_rate) * -60  # Example loudness data

# Initialize plot
fig, ax = plt.subplots()
line, = ax.plot(times, loudness, label='Loudness')
dot, = ax.plot([], [], 'ro')  # Red dot to show current position

ax.set_xlim(0, song_duration)
ax.set_ylim(np.min(loudness), np.max(loudness))

def update(frame):
        # Update the dot's position to simulate progress
        dot.set_data(times[frame], loudness[frame])
        return dot,

def play_song():
    pygame.mixer.music.play()

def start_animation(times):
    # Start the song in a separate thread
    threading.Thread(target=play_song).start()
    # Start the animation
    ani = FuncAnimation(fig, update, frames=range(len(times)), blit=True, interval=1000/sample_rate)
    plt.show()

# if track_info['tracks']['items']:
initialize_audio('shape.mp3')
start_animation(times)