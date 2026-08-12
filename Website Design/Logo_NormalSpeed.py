# totalrecalls_multicolor_16beams.py
# Multi-Color Transparent Vortex Animation — TotalRecalls.app
# Author: Andre

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(6, 6))
ax = plt.axes()
ax.set_facecolor("none")
fig.patch.set_alpha(0)
ax.axis("off")

# Same 16-color palette as hyper-speed version
beam_colors = [
    "#A070FF", "#FFB84A", "#4BE1D4", "#00C2C7", "#3A7BFF",
    "#FF4BF0", "#D14BFF", "#8B4BFF", "#6BE8FF",
    "#A8FF4B", "#FFE84B", "#FF4B6B", "#FF6B3A",
    "#3AFFC2", "#4BFF8B", "#C8E6FF"
]

# Beam origins in a circle
angles = np.linspace(0, 2*np.pi, 16, endpoint=False)
beam_origins = [(2.5*np.cos(a), 2.5*np.sin(a)) for a in angles]

beam_lines = []

for color in beam_colors:
    line, = ax.plot([], [], color=color, linewidth=2.5, alpha=0.9)
    beam_lines.append(line)

# Draw grid
outer_color = "#1E1F22"
center_color = "#3A7BFF"
spacing = 1.2
square_size = 0.6

for i in range(3):
    for j in range(3):
        x = (i - 1) * spacing
        y = (j - 1) * spacing
        color = center_color if (i == 1 and j == 1) else outer_color
        rect = plt.Rectangle((x - square_size/2, y - square_size/2),
                             square_size, square_size,
                             color=color, ec=None)
        ax.add_patch(rect)

# Glow
glow = plt.Circle((0, 0), 0.45, color=center_color, alpha=0.9)
ax.add_patch(glow)

# Normal-speed loop
def animate(frame):
    t = np.linspace(0, 1, 120)
    progress = (np.sin(frame / 12) + 1) / 2

    for idx, (x0, y0) in enumerate(beam_origins):
        x_curve = (1 - t)**2 * x0 + 2*(1 - t)*t*(x0 * 0.3) + t**2 * 0
        y_curve = (1 - t)**2 * y0 + 2*(1 - t)*t*(y0 * 0.3) + t**2 * 0

        end_idx = int(progress * len(t))
        beam_lines[idx].set_data(x_curve[:end_idx], y_curve[:end_idx])

    glow.set_alpha(0.5 + 0.5 * np.sin(frame / 10))

    return beam_lines + [glow]

anim = FuncAnimation(fig, animate, frames=240, interval=35, blit=True)

# Transparent MP4
anim.save("totalrecalls_multicolor_16beams.mp4",
          fps=30, dpi=200, codec="libx264",
          extra_args=["-pix_fmt", "yuva420p"])

# Transparent GIF
anim.save("totalrecalls_multicolor_16beams.gif",
          fps=20, dpi=120, writer="imagemagick")

plt.tight_layout()
plt.show()
