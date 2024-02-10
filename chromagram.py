import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pdb
# Example data (simplified for demonstration)
# times = np.array([0, 1, 2])  # Start times of each segment (in seconds)
# pitches = np.array([
#     [0.7, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.5],  # Chroma vector for segment 1
#     [0.5, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.7, 0.9],  # Chroma vector for segment 2
#     [0.9, 0.7, 0.1, 0.3, 0.5, 0.2, 0.8, 0.6, 0.4, 0.9, 0.7, 0.5]   # Chroma vector for segment 3
# ])

def chroma(times, input_pitches):
    # pdb.set_trace()
    pitches = np.array(input_pitches)
    # Setup the circular chromagram plot
    num_pitches = pitches.shape[1]
    angles = np.linspace(0, 2 * np.pi, num_pitches, endpoint=False)
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    colors = cm.viridis(np.linspace(0, 1, num_pitches))  # Color map for visualizing intensity

    # Plot each chroma vector
    for i, chroma in enumerate(pitches):
        for j, intensity in enumerate(chroma):
            ax.plot([angles[j], angles[j]], [0, intensity], color=colors[j], linewidth=2)

    # Adjust aesthetics
    ax.set_xticks(angles)
    pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    ax.set_xticklabels(pitch_classes)
    plt.title('Circular Chromagram')

    plt.show()
