import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection


class RobotPath:
    def __init__(self, robot_path, human_cluster, obstacle, human, complaint):
        self.robot_path = robot_path
        self.human_cluster = human_cluster
        self.obstacle = obstacle
        self.human = human
        self.h = human[0]
        self.complaint = complaint
        self.nx = np.shape(self.robot_path)[0] // 2


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
    alpha = [0.2, 1]
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
            p = PatchCollection(patches, facecolors=color[i], edgecolors=color[i], alpha=alpha[i])
            ax.add_collection(p)


def animate(i, ax, particles, particles_zone, cls_robot_path, period_template, period_text, complaint_template,
            complaint_text, q):
    cls_robot_path.h = cls_robot_path.human[i]
    period_text.set_text(period_template % i)
    complaint_text.set_text(complaint_template % cls_robot_path.complaint[i])

    particles.set_offsets(cls_robot_path.h)
    particles_zone.set_offsets(cls_robot_path.h)

    x = np.reshape(cls_robot_path.robot_path[:, i][0:cls_robot_path.nx], (cls_robot_path.nx, 1))
    y = np.reshape(cls_robot_path.robot_path[:, i][cls_robot_path.nx:2*cls_robot_path.nx], (cls_robot_path.nx, 1))
    q.set_offsets(np.hstack([x, y])[:-1, :])
    q.set_UVC(x[1:] - x[:-1], y[1:] - y[:-1])

    ax.set_xlim((min([min(x), 0]), max(x)))
    ax.set_ylim((min([min(y), 0]), max(y)))

    return [particles] + [period_text] + [complaint_text] + [q]


def vis(human_cluster, obstacle, human_period, x_period, complaint_period):
    cls_robot_path = RobotPath(x_period, human_cluster, obstacle, human_period, complaint_period)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.yaxis.tick_right()
    workspace_plot(ax, human_cluster, obstacle)
    period_template = 'period = %d'
    period_text = ax.text(0.01, 1.05, period_template % 0, transform=ax.transAxes, weight='bold')
    complaint_template = 'complaints = %d'
    complaint_text = ax.text(0.35, 1.05, complaint_template % 0, transform=ax.transAxes, weight='bold')

    particles = ax.scatter([], [], c='tab:blue', s=10, cmap="hsv", vmin=0, vmax=1)
    particles_zone = ax.scatter([], [], facecolors="None", edgecolors='tab:orange', s=200, cmap="hsv", vmin=0, vmax=1,
                                alpha=1)

    q = ax.quiver(np.zeros((cls_robot_path.nx-1, 1)), np.zeros((cls_robot_path.nx-1, 1)), [], [], scale_units='xy',
                  angles='xy', scale=1, color='r')

    max_frame = np.shape(x_period)[1]
    ani = anim.FuncAnimation(fig, animate, fargs=[ax, particles, particles_zone, cls_robot_path, period_template,
                                                  period_text, complaint_template, complaint_text, q],
                             frames=max_frame, interval=30, blit=True, repeat=False)
    ani.save('/Users/chrislaw/Github/SocialRobotHumanFeedback/video/online.mp4', fps=0.5, dpi=400)

    plt.show()