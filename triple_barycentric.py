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
sim.add(m=1.0, a=5, e=0.0, inc=0)  # Orbiting star A
# Star C
sim.add(m=1.0, a=50, e=0.5, inc=.2)  # Orbiting the center of mass of A and B

# Shift to the center of mass frame
sim.move_to_com()

# Choose an integrator
sim.integrator = "ias15" 

Pinner = sim.particles[1].P
Pouter = sim.particles[2].P

# Run the simulation
times = np.arange(0, 3*Pouter, 4)

Noutputs = len(times)
x = np.zeros((3,Noutputs))
y = np.zeros((3,Noutputs))
z = np.zeros((3,Noutputs))

print(Noutputs)

grid = 20

# Plot the results
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')

# Set the background color to black
ax.set_facecolor('black')
fig.set_facecolor('black')
ax.w_xaxis.pane.fill = False
ax.w_yaxis.pane.fill = False
ax.w_zaxis.pane.fill = False

# Define the update function for the animation
def update(num):
    sim.integrate(times[num])

    x[0][num] = sim.particles[0].x
    y[0][num] = sim.particles[0].y
    z[0][num] = sim.particles[0].z
    x[1][num] = sim.particles[1].x
    y[1][num] = sim.particles[1].y
    z[1][num] = sim.particles[1].z
    x[2][num] = sim.particles[2].x
    y[2][num] = sim.particles[2].y
    z[2][num] = sim.particles[2].z

    ax.cla()
    ax.plot(x[0][:num], y[0][:num], z[0][:num], color="dodgerblue", alpha=.8, linewidth=.75)
    ax.plot(x[1][:num], y[1][:num], z[1][:num], color="green", alpha=.8, linewidth=.75)
    ax.plot(x[2][:num], y[2][:num], z[2][:num], color="white", alpha=.8, linewidth=.75)

    ax.grid(False)
    ax.set_frame_on(False)
    ax.set_axis_off()
    ax.set_xlim([-1.5*grid,grid])
    ax.set_ylim([-1.5*grid,grid])
    ax.set_zlim([-grid,grid])

# Create the animation
ani = FuncAnimation(fig, update, frames=Noutputs, repeat=True)

# Save the animation as a GIF
ani.save('triple_barycentric.gif', writer=PillowWriter(fps=30))

plt.close()