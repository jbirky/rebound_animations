import rebound
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
from scipy.optimize import fsolve

from matplotlib import rc
rc('text', usetex=True)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)



sim = rebound.Simulation()
sim.G = 6.674e-11
sim.units = ('AU', 'yr', 'Msun')
sim.add(m=1.4)  # Star 1
sim.add(m=0.3, a=5, e=0.5, omega=120*np.pi/180)  # Star 2
sim.add(m=0.01, a=50, e=0.0, inc=70*np.pi/180, omega=0)  # Star 3
sim.move_to_com() 
sim.integrator = "ias15" 

times = np.arange(0, 1e6, 5e3)
Noutputs = len(times)
print(len(times))

# Create arrays to store eccentricities and inclinations
ecc1 = np.zeros(len(times))
inc1 = np.zeros(len(times))
ecc2 = np.zeros(len(times))
inc2 = np.zeros(len(times))
semi1 = np.zeros(len(times))
semi2 = np.zeros(len(times))
Manom1 = np.zeros(len(times))
Manom2 = np.zeros(len(times))

# Create the 3D plot
fig = plt.figure(figsize=(18,6))
ax = fig.add_subplot(131, projection='3d')
ax_ecc = fig.add_subplot(132)
ax_inc = fig.add_subplot(133)

# Set the background color to black
ax.set_facecolor('black')
ax_ecc.set_facecolor('black')
ax_inc.set_facecolor('black')
fig.set_facecolor('black')
ax.w_xaxis.pane.fill = False
ax.w_yaxis.pane.fill = False
ax.w_zaxis.pane.fill = False

grid = 15
ax.set_axis_off()
ax.set_xlim([-1.5*grid,grid])
ax.set_ylim([-1.5*grid,grid])
ax.set_zlim([-grid,grid])

def calc_coordinates(sim, particle):
    # Define the semi-major and semi-minor axes
    a = sim.particles[particle].a
    ecc = sim.particles[particle].e
    inc = sim.particles[particle].inc
    M = sim.particles[particle].M

    # Define Kepler's equation
    def kepler(E):
        return E - ecc*np.sin(E) - M

    # Solve Kepler's equation for the eccentric anomaly
    E = fsolve(kepler, M)

    # true anomaly
    f = np.arange(0, 2*np.pi, 0.01)

    # Calculate the radius
    r = a * (1 - ecc*np.cos(E))

    # Calculate the Cartesian coordinates
    x = r * (np.cos(f) * np.cos(inc))
    y = r * np.sin(f)
    z = r * (np.cos(f) * np.sin(inc))

    return x, y, z

# Define the update function for the animation
def update(num):
    sim.integrate(times[num])

    # Define the x and y coordinates of the points on the ellipse
    x1, y1, z1 = calc_coordinates(sim, 1)
    x2, y2, z2 = calc_coordinates(sim, 2)

    # Store eccentricities and inclinations
    ecc1[num] = sim.particles[1].e
    inc1[num] = sim.particles[1].inc
    ecc2[num] = sim.particles[2].e
    inc2[num] = sim.particles[2].inc
    semi1[num] = sim.particles[1].a
    semi2[num] = sim.particles[2].a
    Manom1[num] = sim.particles[1].M
    Manom2[num] = sim.particles[2].M

    ax.cla()
    ax.plot(x1, y1, z1, color="red")
    ax.plot(x2, y2, z2, color="skyblue")

    ax.set_xlim([-grid,grid])
    ax.set_ylim([-grid,grid])
    ax.set_zlim([-grid,grid])

    times_scaled = times / 1e6
    inc_deg1 = inc1 * 180 / np.pi
    inc_deg2 = inc2 * 180 / np.pi
    
    ax_ecc.cla()
    ax_ecc.plot(times_scaled[:num+1], ecc1[:num+1], color="red")
    ax_ecc.plot(times_scaled[:num+1], ecc2[:num+1], color="skyblue")
    ax_ecc.set_xlabel("Time [Myr]", color='white', fontsize=16)
    ax_ecc.set_ylabel("Eccentricity", color='white', fontsize=16)
    ax_ecc.set_xlim([min(times_scaled), max(times_scaled)])
    ax_ecc.set_ylim([0, 0.7])
    ax_ecc.grid(True) 
    ax_ecc.tick_params(axis='both', which='both', direction='in', colors='white', labelsize=20, pad=20)
    ax_ecc.axhline(0, color='white') 

    ax_inc.cla()
    ax_inc.plot(times_scaled[:num+1], inc_deg1[:num+1], color="red")
    ax_inc.plot(times_scaled[:num+1], inc_deg2[:num+1], color="skyblue")
    ax_inc.set_xlabel("Time [Myr]", color='white', fontsize=16)
    ax_inc.set_ylabel("Inclination [deg]", color='white', fontsize=16)
    ax_inc.set_xlim([min(times_scaled), max(times_scaled)])
    ax_inc.set_ylim([0, 180])
    ax_inc.grid(True) 
    ax_inc.tick_params(axis='both', which='both', direction='in', colors='white', labelsize=20, pad=20)
    ax_inc.axhline(0, color='white') 
    
    plt.tight_layout() 

# Create the animation
ani = FuncAnimation(fig, update, frames=Noutputs, repeat=True)

# Save the animation as a GIF
ani.save('kozai_lidov.gif', writer=PillowWriter(fps=30))

plt.close()