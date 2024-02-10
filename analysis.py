import pdb
import matplotlib.pyplot as plt
import pygame
import threading
from matplotlib.animation import FuncAnimation
import numpy as np
from chromagram import chroma
from video import create_animated_chromagram

song_duration = 234  # Example: 5 minutes song
sample_rate = 1  # Update plot every second
fig, ax = plt.subplots()
dot, = ax.plot([], [], 'ro')  # Red dot to show current position

def initialize_audio(audio_file):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)

def get_duration_of_segments(segments):
    duration = sum([float(segment['duration']) for segment in segments])
    return duration

def merge_segments(segments, step=2):
    grouped = []
    for i in range(0, len(segments), step):
        element = {}
        element['start'], combined_segments = segments[i]['start'], segments[i:i+step]
        element['duration'] = get_duration_of_segments(combined_segments)
        element['loudness_start'], element['loudness_end'] = segments[i]['loudness_start'], segments[min(len(segments)-1, i+step-1)]['loudness_start']
        grouped.append(element)
    return grouped

def get_loudness_change(segments):
    # segments = merge_segments(segments, 4)
    durations = [segment['start'] for segment in segments]
    # loudness = [segment['loudness'] for segment in segments]
    loudness = [(segment['loudness_start'] + segment['loudness_end']) / 2 for segment in segments]
    pitches = [segment['pitches'] for segment in segments]
    return durations, pitches

def analyze(track_details):
    segments = track_details.get('segments')
    durations, pitches = get_loudness_change(segments)
    # vis(durations, loudness)
    # plt.plot(durations, loudness)
    # plt.show()
    # pdb.set_trace()
    create_animated_chromagram(durations, np.array(pitches), save_filename='chroma.mp4')
    # return durations, loudness

# Global variables for simplicity
current_pos = 0  # Current position in the plot

# def on_click(event):
#     global current_pos
#     if event.inaxes is not None:
#         current_pos = event.xdata  # Update the current position based on click
#         # Logic to play audio from current_pos
#         print(f"Playing at position: {current_pos}")
#         # Seek to the position in the audio file (assuming seconds)
#         pygame.mixer.music.play(start=int(current_pos))

# def plot_loudness_over_time(times, loudness):
#     fig, ax = plt.subplots()
#     ax.plot(times, loudness)
#     fig.canvas.mpl_connect('button_press_event', on_click)
#     plt.show()

# def update(frame):
#     # Update the dot's position to simulate progress
#     dot.set_data(times[frame], loudness[frame])
#     return dot,

# def update(dot, times, loudness, frame):
    
#     # Update the dot's position to simulate progress
#     dot.set_data(times[frame], loudness[frame])
#     return dot,

# def play_song():
#     pygame.mixer.music.play()

# # def start_animation():
# #     # Start the song in a separate thread
# #     threading.Thread(target=play_song).start()
# #     # Start the animation
# #     ani = FuncAnimation(fig, update, frames=range(len(times)), blit=True, interval=1000/sample_rate)
# #     plt.show()

# # start_animation()

# def vis(times, loudness):
# # Example usage
#     threading.Thread(target=play_song).start()
#     # Start the animation
#     line, = ax.plot(times, loudness, label='Loudness')
#     ax.set_xlim(0, song_duration)
#     ax.set_ylim(np.min(loudness), np.max(loudness))
#     ani = FuncAnimation(fig, update, frames=range(len(times)), blit=True, interval=1000/sample_rate)
#     initialize_audio('shape.mp3')
#     plot_loudness_over_time(times, loudness)