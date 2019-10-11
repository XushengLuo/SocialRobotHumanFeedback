# -*- coding: utf-8 -*-

from random import randint
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np
import random
import sys


class Workspace(object):
    """
    define the workspace where robots reside
    """
    def __init__(self):
        # dimension of the workspace
        # self.length = int(sys.argv[1])
        # self.width = int(sys.argv[1])
        # n = int(sys.argv[2])
        self.length = 20
        self.width = 20
        self.workspace = (self.length, self.width)
        self.num_of_regions = 4
        self.num_of_obstacles = 0
        self.occupied = []
        self.regions = {'l{0}'.format(i+1): j for i, j in enumerate(self.allocate(self.num_of_regions))}
        self.obstacles = {'o{0}'.format(i+1): j for i, j in enumerate(self.allocate(self.num_of_obstacles))}

        self.graph_workspace = nx.Graph()
        self.build_graph()
        self.init_goal = {}

    def allocate(self, num):
        obj = []
        dis = 0
        local = 4
        x = 5
        y = 13
        cand = [(x, x), (x, y), (y, x), (y, y)]
        for i in range(num):
            while True:
                # candidate = (randint(0, self.width-1), randint(0, self.length-1))
                candidate = cand[i]
                if candidate in self.occupied and \
                        len([o for o in obj if abs(o[0]-candidate[0]) >= dis and abs(o[1]-candidate[1]) >= dis]) != len(obj):
                    continue
                else:
                    obj.append(candidate)
                    break
            self.occupied.append(candidate)

        for i in range(num):
            for j in range(3):
                while True:
                    candidate = (randint(obj[i][0] - local, obj[i][0] + local),
                                 randint(obj[i][1] - local, obj[i][1] + local))
                    if candidate in self.occupied:
                        continue
                    else:
                        obj.append(candidate)
                        break
                self.occupied.append(candidate)
        return obj

    def reachable(self, location):
        next_location = []
        obstacles = list(self.obstacles.values())
        # left
        if location[0]-1 >= 0 and (location[0]-1, location[1]) not in obstacles:
            next_location.append((location, (location[0]-1, location[1])))
        # right
        if location[0]+1 <= self.width and (location[0]+1, location[1]) not in obstacles:
            next_location.append((location, (location[0]+1, location[1])))
        # up
        if location[1]+1 <= self.length and (location[0], location[1]+1) not in obstacles:
            next_location.append((location, (location[0], location[1]+1)))
        # down
        if location[1]-1 >= 0 and (location[0], location[1]-1) not in obstacles:
            next_location.append((location, (location[0], location[1]-1)))
        return next_location

    def build_graph(self):
        obstacles = list(self.obstacles.values())
        for i in range(self.width):
            for j in range(self.length):
                if (i, j) not in obstacles:
                    self.graph_workspace.add_edges_from(self.reachable((i, j)))

    def plot_workspace(self):
        ax = plt.figure(1).gca()
        ax.set_xlim((0, self.width))
        ax.set_ylim((0, self.length))
        plt.xticks(np.arange(0, self.width + 1, 1.0))
        plt.yticks(np.arange(0, self.length + 1, 1.0))
        self.plot_workspace_helper(ax, self.regions, 'region')
        self.plot_workspace_helper(ax, self.init_goal, 'obstacle')

    def plot_workspace_helper(self, ax, obj, obj_label):
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        plt.gca().set_aspect('equal', adjustable='box')
        # plt.grid(b=True, which='major', color='k', linestyle='--')
        for key in obj:
            color = '0.75' if obj_label != 'region' else 'c'
            x = []
            y = []
            x_ = obj[key][0]
            y_ = obj[key][1]
            patches = []
            for point in [(x_, y_), (x_+1, y_), (x_+1, y_+1), (x_, y_+1)]:
                x.append(point[0])
                y.append(point[1])
            polygon = Polygon(np.column_stack((x, y)), True)
            patches.append(polygon)
            p = PatchCollection(patches, facecolors=color, edgecolors=color)
            ax.add_collection(p)
            ax.text(np.mean(x)-0.2, np.mean(y)-0.2, r'${}_{{{}}}$'.format(key[0], key[1:]), fontsize=8)

    def path_plot(self, robot_path):
        """
        plot the path
        :param path: found path
        :param workspace: workspace
        :param number_of_robots:
        :return: figure
        """

        for robot, path in robot_path.items():
            # prefix path
            if len(path) == 1:
                continue
            x_pre = np.asarray([point[0] + 0.5 for point in path])
            y_pre = np.asarray([point[1] + 0.5 for point in path])
            plt.quiver(x_pre[:-1], y_pre[:-1], x_pre[1:] - x_pre[:-1], y_pre[1:] - y_pre[:-1],
                       color="#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]),
                       scale_units='xy', angles='xy', scale=1, label='prefix path')

            plt.savefig('img/path.png', bbox_inches='tight', dpi=600)