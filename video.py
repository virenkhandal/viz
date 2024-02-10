import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.cm as cm

def create_animated_chromagram(times, pitches, save_filename=None):
    """
    Creates an animated circular chromagram.

    Parameters:
    - times: Array of start times for each segment.
    - pitches: 2D array of chroma vectors for each segment.
    - save_filename: Optional; if provided, the animation is saved to this file.
    """
    # Setup plot
    num_pitches = pitches.shape[1]
    angles = np.linspace(0, 2 * np.pi, num_pitches, endpoint=False)
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_xticks(angles)
    pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    ax.set_xticklabels(pitch_classes)
    plt.title('Animated Circular Chromagram')

    colors = cm.viridis(np.linspace(0, 1, num_pitches))  # Color map
    lines = [ax.plot([], [], color=colors[j], linewidth=2)[0] for j in range(num_pitches)]

    def init():
        """Initial plot setup."""
        for line in lines:
            line.set_data([], [])
        return lines

    def animate(i):
        """Update the plot for each frame."""
        for j, line in enumerate(lines):
            intensity = pitches[i, j]
            line.set_data([angles[j], angles[j]], [0, intensity])
        return lines

    anim = FuncAnimation(fig, animate, init_func=init, frames=len(times), interval=1000, blit=True)

    if save_filename:
        anim.save(save_filename, fps=5, extra_args=['-vcodec', 'libx264'])

    plt.close()  # Prevents the static plot from displaying
