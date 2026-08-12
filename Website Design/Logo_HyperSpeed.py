# totalrecalls_hyperspeed_16beams.py
# Hyper-Speed Transparent Vortex Animation — TotalRecalls.app
# Author: Andre

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Transparent figure
fig = plt.figure(figsize=(6, 6))
ax = plt.axes()
ax.set_facecolor("none")
fig.patch.set_alpha(0)
ax.axis("off")

# Grid parameters
grid_size = 3
spacing = 1.2
square_size = 0.6

# Provider colors (5)
provider_colors = [
    "#A070FF",  # OpenAI
    "#FFB84A",  # Claude
    "#4BE1D4",  # Perplexity
    "#00C2C7",  # Gemini
    "#3A7BFF"   # DeepSeek
]

# Additional 11 colors (other providers)
extra_colors = [
    "#FF4BF0", "#D14BFF", "#8B4BFF", "#6BE8FF",
    "#A8FF4B", "#FFE84B", "#FF4B6B", "#FF6B3A",
    "#3AFFC2", "#4BFF8B", "#C8E6FF"
]

# Full 16-beam palette
beam_colors = provider_colors + extra_colors

# Generate 16 beam origins in a circle
angles = np.linspace(0, 2*np.pi, 16, endpoint=False)
beam_origins = [(2.5*np.cos(a), 2.5*np.sin(a)) for a in angles]

beam_lines = []

# Initialize beams
for color in beam_colors:
    line, = ax.plot([], [], color=color, linewidth=2.5, alpha=0.9)
    beam_lines.append(line)

# Draw grid squares
outer_color = "#1E1F22"
center_color = "#3A7BFF"

for i in range(grid_size):
    for j in range(grid_size):
        x = (i - 1) * spacing
        y = (j - 1) * spacing
        color = center_color if (i == 1 and j == 1) else outer_color
        rect = plt.Rectangle((x - square_size/2, y - square_size/2),
                             square_size, square_size,
                             color=color, ec=None)
        ax.add_patch(rect)

# Central glow
glow = plt.Circle((0, 0), 0.45, color=center_color, alpha=0.9)
ax.add_patch(glow)

# Hyper-speed animation
def animate(frame):
    t = np.linspace(0, 1, 120)

    # Very fast loop
    progress = (np.sin(frame / 6) + 1) / 2

    for idx, (x0, y0) in enumerate(beam_origins):
        # Curved inward path
        x_curve = (1 - t)**2 * x0 + 2*(1 - t)*t*(x0 * 0.3) + t**2 * 0
        y_curve = (1 - t)**2 * y0 + 2*(1 - t)*t*(y0 * 0.3) + t**2 * 0

        end_idx = int(progress * len(t))
        beam_lines[idx].set_data(x_curve[:end_idx], y_curve[:end_idx])

    # Faster glow pulse
    glow.set_alpha(0.5 + 0.5 * np.sin(frame / 5))

    return beam_lines + [glow]

anim = FuncAnimation(fig, animate, frames=240, interval=25, blit=True)

# Transparent MP4
anim.save("totalrecalls_hyperspeed_16beams.mp4",
          fps=30, dpi=200, codec="libx264",
          extra_args=["-pix_fmt", "yuva420p"])

# Transparent GIF
anim.save("totalrecalls_hyperspeed_16beams.gif",
          fps=20, dpi=120, writer="imagemagick")

plt.tight_layout()
plt.show()
