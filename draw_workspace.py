import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from termcolor import colored
import matplotlib
import random


def workspace_plot(path, nx, obstacle, measure, human, human_scale):
    """
    plot the workspace
    :return: figure
    """
    ax = plt.figure().gca()

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(b=True, which='major', color='k', linestyle='--')

    c = {'x': 'r', 'x_m': 'g'}
    # c = {r'$\mathbf{x}_0$': 'r', r'$\mathbf{x}_{\mathrm{zero}}$': 'g', r'$\mathbf{x}_{\mathrm{MPC}}$': 'b'}

    for key, value in path.items():
        x_pre = value[0:nx]
        y_pre = value[nx:2 * nx]
        # c = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        plt.quiver(x_pre[:-1], y_pre[:-1], x_pre[1:] - x_pre[:-1], y_pre[1:] - y_pre[:-1], color=c[key],
                   scale_units='xy', angles='xy', scale=1, label=r'${0}$'.format(key))
        # plt.quiver(x_pre[:-1], y_pre[:-1], x_pre[1:] - x_pre[:-1], y_pre[1:] - y_pre[:-1], color=c[key],
        #        scale_units='xy', angles='xy', scale=1)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.legend([r'$\mathbf{x}_0$', r'$\mathbf{x}_{\mathrm{zero}}$', r'$\mathbf{x}_{\mathrm{MPC}}$'], fontsize=14,
    #            loc='center left', bbox_to_anchor=(1, 0.5))

    obj = [{}, obstacle]
    color = ['c', 'r']
    alpha = [0.4, 1]
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

    if human:
        xh = [h[0] for h in human]
        yh = [h[1] for h in human]
        plt.plot(xh, yh, 'bo', markersize=3)
        for i in range(len(xh)):
            circle = plt.Circle((xh[i], yh[i]), human_scale[i], color='r', fill=False)
            ax.add_artist(circle)
    ax.set_xlim((min([min(x_pre), 0]), max(x_pre)))
    ax.set_ylim((min([min(y_pre), 0]), max(y_pre)))
    # ax.set_xlim((0, 20))
    # ax.set_ylim((0, 20))

    plt.xticks([0, 5, 10, 15, 20], fontsize=16, usetex=True)
    plt.yticks([0, 5, 10, 15, 20], fontsize=16, usetex=True)

    matplotlib.rcParams.update({'font.size': 16})