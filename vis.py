import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection


class RobotPath:
    def __init__(self, robot_path, human_cluster, obstacle, human):
        self.robot_path = robot_path
        self.human_cluster = human_cluster
        self.obstacle = obstacle
        self.human = human
        self.h = human[0]


def workspace_plot(ax, polygon, obstacle):
    """
    plot the workspace
    :return: figure
    """
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(b=True, which='major', color='k', linestyle='--')

    obj = [polygon, obstacle]
    color = ['c', 'r']
    for i, o in enumerate(obj):
        for poly in o.values():
            x = []
            y = []
            patches = []
            for point in poly:
                x.append(point[0])
                y.append(point[1])
            polygon = Polygon(np.column_stack((x, y)), True)
            patches.append(polygon)
            p = PatchCollection(patches, facecolors=color[i], edgecolors=color[i])
            ax.add_collection(p)


def animate(i, particles, particles_zone, cls_robot_path, period_template, period_text):
    cls_robot_path.h = cls_robot_path.human[i]
    period_text.set_text(period_template % i)

    particles.set_offsets(cls_robot_path.h)
    particles_zone.set_offsets(cls_robot_path.h)

    return [particles]+[period_text]


def vis(human_cluster, obstacle, human_period, x_period):
    cls_robot_path = RobotPath(x_period, human_cluster, obstacle, human_period)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.yaxis.tick_right()
    workspace_plot(ax, human_cluster, obstacle)
    period_template = 'period = %d'
    period_text = ax.text(0.01, 1.05, period_template % 0, transform=ax.transAxes, weight='bold')

    particles = ax.scatter([], [], c='tab:blue', s=10, cmap="hsv", vmin=0, vmax=1, alpha=1)
    particles_zone = ax.scatter([], [], c='tab:orange', s=200, cmap="hsv", vmin=0, vmax=1, alpha=0.1)

    max_frame = np.shape(x_period)[1]
    ani = anim.FuncAnimation(fig, animate, fargs=[particles, particles_zone, cls_robot_path, period_template, period_text],
                             frames=max_frame, interval=30, blit=True, repeat=False)
    ani.save('/Users/chrislaw/Github/SocialRobotHumanFeedback/video/online.mp4', fps=1, dpi=400)

    # plt.show()