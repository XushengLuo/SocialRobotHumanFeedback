import numpy as np
from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as pl
from matplotlib.collections import PatchCollection
import random
import sys


# def get_cluster(human_cluster):
#     point_cluster = {key: [] for key in human_cluster.keys()}
#     human = []
#     num_human = 50  # int(sys.argv[1])
#     i = 0
#     while i < num_human:
#         p = np.random.random((1, 2))[0] * 20
#         for index, polygon in human_cluster.items():
#             cluster = Polygon(polygon)
#             if Point((p[0], p[1])).within(cluster):
#                 human.append((p[0], p[1]))
#                 point_cluster[index].append((p[0], p[1]))
#                 i += 1
#                 break
#     num_scale = 5
#     scale = np.linspace(0.2, 0.2+(num_scale-1)*0.1, num_scale)
#     human_scale = scale[np.random.randint(0, num_scale, len(human))]
#     return human, point_cluster, human_scale


def get_cluster(obstacle):
    human = []
    num_human = 50  # int(sys.argv[1])
    i = 0
    while i < num_human:
        collision = 0
        p = np.random.random((1, 2))[0] * 20
        if np.linalg.norm(np.subtract(p, (0, 0))) > 2 and np.linalg.norm(np.subtract(p, (20, 20))) > 2:
            for index, polygon in obstacle.items():
                obs = Polygon(polygon)
                if Point((p[0], p[1])).within(obs):
                    collision = 1
                    break
            if not collision:
                human.append((p[0], p[1]))
                i += 1

    num_scale = 4
    scale = np.linspace(0.3, 0.2+(num_scale-1)*0.1, num_scale)
    human_scale = scale[np.random.randint(0, num_scale, len(human))]
    return human, human_scale


def update_cluster(human, obstacle):
    new_human = []
    radius = 1  # float(sys.argv[2])
    for h in human:
        while True:
            ut = np.random.random((2, 1)) * 2 - 1
            ut = ut/np.linalg.norm(ut)
            p = (h[0]+ut[0][0]*random.uniform(0, radius), h[1]+ut[1][0]*random.uniform(0, radius))
            if 0 <= p[0] <= 20 and 0 <= p[1] <= 20:
                if np.linalg.norm(np.subtract(p, (0, 0))) > 2 and np.linalg.norm(np.subtract(p, (20, 20))) > 2:
                    collision = 0
                    for index, polygon in obstacle.items():
                        obs = Polygon(polygon)
                        if Point((p[0], p[1])).within(obs):
                            collision = 1
                            break
                    if not collision:
                        new_human.append(p)
                        break

    num_scale = 4
    scale = np.linspace(0.3, 0.2 + (num_scale - 1) * 0.1, num_scale)
    human_scale = scale[np.random.randint(0, num_scale, len(human))]
    return new_human, human_scale

# human_cluster = {1: [(5, 5), (8, 3), (9, 3), (9, 4), (7, 7), (5, 7)],
#                  2: [(13, 5), (15, 1), (16, 1), (16, 4), (14, 6), (13, 6)],
#                  3: [(14, 9), (18, 9), (18, 10), (14, 10)],
#                  4: [(10, 12), (11, 12), (14, 13), (14, 14), (11, 16), (10, 16)],
#                  5: [(5, 13), (6, 13), (6, 16), (3, 17), (2, 17), (2, 15)]}
# human, point_cluster = get_cluster(human_cluster)
# xh = [h[0] for h in human]
# yh = [h[1] for h in human]
#
# ax = plt.figure().gca()
#
# plt.rc('text', usetex=True)
# plt.rc('font', family='serif')
# plt.gca().set_aspect('equal', adjustable='box')
# plt.grid(b=True, which='major', color='k', linestyle='--')
#
# # plt.plot(path[0:nx], path[nx:2*nx], 'ro', markersize=3)
#
# obj = [human_cluster]
# color = ['c', 'r']
# for i, o in enumerate(obj):
#     for poly in o.values():
#         x = []
#         y = []
#         patches = []
#         for point in poly:
#             x.append(point[0])
#             y.append(point[1])
#         polygon = pl(np.column_stack((x, y)), True)
#         patches.append(polygon)
#         p = PatchCollection(patches, facecolors=color[i], edgecolors=color[i])
#         ax.add_collection(p)
#
# plt.plot(xh, yh, 'bo', markersize=2)
# for i in range(len(xh)):
#     circle = plt.Circle((xh[i], yh[i]), 0.4, color='r', fill=False)
#     ax.add_artist(circle)
# plt.show()
