import functions
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
sys.path.append(r"D:\My_Code")

# def f(x,y):
#     "Objective function"
#     return (x-3.14)**2 + (y-2.72)**2 + np.sin(3*x+1.41) + np.sin(4*y-1.73)

# Compute and plot the function in 3D within [0,5]x[0,5]
# x = np.array(np.meshgrid(nplinspace()))
# z = f(x,name='Sphere', dim=10)

# Find the global minimum
# x_min = x.ravel()[z.argmin()]
global Velocity, X_pos, pbest, pbest_obj, gbest, gbest_obj
def update(dc,str_with_copies,w,c1,c2,particl_dim,swarm_size,Velocity,gbest,pbest,X_pos,pbest_obj):
    "Function to do one iteration of particle swarm optimization"
    # Update params
    r1, r2 = np.random.rand(2)
    Velocity = w * Velocity + c1*r1 * \
        (pbest - X_pos) + c2*r2*(gbest.reshape(-1, 1)-X_pos)
    sigV = 1/(1+(np.exp((-Velocity))))
    X_pos = (sigV > np.random.rand(particl_dim, swarm_size)).astype(int)
    obj = []
    for i in range(swarm_size):
        ####################################################
        temp_x=np.array(str_with_copies)
        np.put(temp_x,dc,X_pos[:, i])
        ####################################################
        obj.append(functions.f(temp_x))
    pbest[:, (pbest_obj >= obj)] = X_pos[:, (pbest_obj >= obj)]
    pbest_obj = np.array([pbest_obj, obj]).min(axis=0)
    gbest = pbest[:, pbest_obj.argmin()]
    gbest_obj = pbest_obj.min()

def opt(dc,str_with_copies):
    # Hyper-parameter of the algorithm
    c1 = c2 = 0.1
    w = 0.8

    # Create particles
    particl_dim = len(dc)
    swarm_size = 100
    np.random.seed(100)
    X_pos = np.round(np.random.rand(particl_dim, swarm_size)).astype(int)
    Velocity = np.random.randn(particl_dim, swarm_size) * 0.1

    # Initialize data
    pbest = X_pos
    pbest_obj = []
    for i in range(swarm_size):
        #############################################
        temp_x=np.array(str_with_copies)
        np.put(temp_x,dc,X_pos[:, i])
        #############################################
        pbest_obj.append(functions.f(temp_x))

    gbest = pbest[:, np.array(pbest_obj).argmin()]
    gbest_obj = np.array(pbest_obj).min()
    iteration = 300


    


    for itr in range(iteration):
        update(dc,str_with_copies,w,c1,c2,particl_dim,swarm_size,Velocity,gbest,pbest,X_pos,pbest_obj)

    # Set up base figure: The contour map
    # fig, ax = plt.subplots(figsize=(8,6))
    # fig.set_tight_layout(True)
    # img = ax.imshow(z, extent=[0, 5, 0, 5], origin='lower', cmap='viridis', alpha=0.5)
    # fig.colorbar(img, ax=ax)
    # ax.plot([x_min], [y_min], marker='x', markersize=5, color="white")
    # contours = ax.contour(x, y, z, 10, colors='black', alpha=0.4)
    # ax.clabel(contours, inline=True, fontsize=8, fmt="%.0f")
    # pbest_plot = ax.scatter(pbest[0], pbest[1], marker='o', color='black', alpha=0.5)
    # p_plot = ax.scatter(X_pos[0], X_pos[1], marker='o', color='blue', alpha=0.5)
    # p_arrow = ax.quiver(X_pos[0], X_pos[1], Velocity[0], Velocity[1], color='blue', width=0.005, angles='xy', scale_units='xy', scale=1)
    # gbest_plot = plt.scatter([gbest[0]], [gbest[1]], marker='*', s=100, color='black', alpha=0.4)
    # ax.set_xlim([0,5])
    # ax.set_ylim([0,5])

    # def animate(i):
    #     "Steps of PSO: algorithm update and show in plot"
    #     title = 'Iteration {:02d}'.format(i)
    #     # Update params
    #     update()
    #     # Set picture
    #     ax.set_title(title)
    #     pbest_plot.set_offsets(pbest.T)
    #     p_plot.set_offsets(X_pos.T)
    #     p_arrow.set_offsets(X_pos.T)
    #     p_arrow.set_UVC(Velocity[0], Velocity[1])
    #     gbest_plot.set_offsets(gbest.reshape(1,-1))
    #     return ax, pbest_plot, p_plot, p_arrow, gbest_plot

    # anim = FuncAnimation(fig, animate, frames=list(range(1,50)), interval=500, blit=False, repeat=True)
    # anim.save("PSO.gif", dpi=120, writer="imagemagick")
    ###############################
    temp=np.array(str_with_copies)
    np.put(temp,dc,gbest)
    temp_lst=temp.tolist()
    ###############################
    x_star="".join(temp_lst)
    return [gbest_obj,x_star]
    print("PSO found best solution at f({})={}".format(gbest, gbest_obj))
#print("Global optimal at f({})={}".format([x_min,y_min], f(x_min,y_min)))
