import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from termcolor import colored


def workspace_plot(path, nx, polygon, obstacle, measure, human):
    """
    plot the workspace
    :return: figure
    """
    ax = plt.figure().gca()

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(b=True, which='major', color='k', linestyle='--')

    # plt.plot(path[0:nx], path[nx:2*nx], 'ro', markersize=3)

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

    x_pre = path[0:nx]
    y_pre = path[nx:2*nx]
    plt.quiver(x_pre[:-1], y_pre[:-1], x_pre[1:] - x_pre[:-1], y_pre[1:] - y_pre[:-1], color='r',
                     scale_units='xy', angles='xy', scale=1)

    if human:
        xh = [h[0] for h in human]
        yh = [h[1] for h in human]
        plt.plot(xh, yh, 'bo', markersize=3)
        for i in range(len(xh)):
            circle = plt.Circle((xh[i], yh[i]), 0.5, color='r', fill=False)
            ax.add_artist(circle)
    ax.set_xlim((min([min(x_pre), 0]), max(x_pre)))
    ax.set_ylim((min([min(y_pre), 0]), max(y_pre)))

    # ax = plt.figure(1).gca()
    # plt.plot(range(2, np.shape(measure)[0]+1), measure[1:])