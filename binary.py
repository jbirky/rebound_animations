import rebound
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)


# Initialize a simulation
sim = rebound.Simulation()

# Star A
sim.add(m=1.0)  # This will be our reference star at the origin
# Star B
sim.add(m=1.0, a=5, e=0.7, inc=0)  # Orbiting star A

# Shift to the center of mass frame
sim.move_to_com()

# Choose an integrator
sim.integrator = "ias15" 

Pinner = sim.particles[1].P

# Run the simulation
times = np.arange(0, 10*Pinner, 1)
Noutputs = len(times)
print(Noutputs)

op = rebound.OrbitPlot(sim, periastron=False, color=True)
op.ax.set_axis_off()
fig = op.fig

for ax in fig.get_axes():
    ax.set_xticks([])
    ax.set_yticks([])
    ax.xaxis.label.set_size(30)  
    ax.yaxis.label.set_size(30)

# Define the update function for the animation
def update(num):
    sim.integrate(times[num])
    op.update(updateLimits=True)
    fig.canvas.draw()

# Create the animation
ani = FuncAnimation(fig, update, frames=Noutputs, repeat=True)

# Save the animation as a GIF
ani.save('binary.gif', writer=PillowWriter(fps=30), dpi=300)

plt.close()