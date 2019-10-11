import numpy as np
from shapely.geometry import Point, LineString, Polygon
from smallest_enclosing_circle import make_circle
from itertools import groupby
from operator import itemgetter


def human_feedback(x, human_cluster, point_cluster, obstacle):
    score = 0
    index = set()
    nx = np.shape(x)[0]//2

    for num, polygon in human_cluster.items():
        point = []
        cluster = Polygon(polygon)
        for i in range(nx - 1):
            # whether the line segment crosses the cluster(polygon)
            if LineString([Point((x[i], x[i+nx])), Point(x[i+1], x[i+1+nx])]).intersects(cluster):
                point.append([(x[i], x[i+nx]), (x[i+1], x[i+1+nx])])
                index.add(i)
                index.add(i+1)
        if point:
            score += get_score_from_human(point, point_cluster[num])
    # obstacle avoidance
    for num, polygon in obstacle.items():
        obs = Polygon(polygon)
        for i in range(nx - 1):
            # whether the line segment crosses the (obstacle)
            if LineString([Point((x[i], x[i + nx])), Point(x[i + 1], x[i + 1 + nx])]).intersects(obs):
                score += 2
                index.add(i)
                index.add(i+1)

    # the length of the trajectory
    dist = np.sum([np.linalg.norm([x[i] - x[i + 1], x[i + nx] - x[i + 1 + nx]]) for i in range(nx - 1)])
    score += dist

    # index
    index_group = []
    index = list(index)
    index.sort()
    for k, g in groupby(enumerate(index), lambda ix: ix[0] - ix[1]):
        index_group.append(list(map(itemgetter(1), g)))
    expand_index = set([j for i in index_group for j in i])
    for group in index_group:
        num = np.random.randint(0, 3)
        extra = [group[0]-k for k in range(1, num+1) if group[0]-k > 0] + \
                [group[-1]+k for k in range(1, num+1) if group[-1]+k < nx]
        expand_index.update(set(extra))
    return score, dist, list(expand_index)


def get_score(point, polygon):
    """
    the distance of the center of polygon to the line segment of a trajectory
    :param point:
    :param polygon:
    :return:
    """
    rho = 1
    cx, cy, r = make_circle(polygon)
    score = 0
    for p in point:
        d = np.abs((p[1][1]-p[0][1])*cx - (p[1][0]-p[0][0])*cy + p[1][0]*p[0][1] - p[1][1]*p[0][0]) / \
            np.sqrt((p[1][1]-p[0][1])**2 + (p[1][0]-p[0][0])**2)
        score += rho/d[0]
    return score


def get_score_from_human(point, point_cluster):
    score = 0
    radius = 0.5
    for human in point_cluster:
        cx = human[0]
        cy = human[1]
        for p in point:
            d = np.abs((p[1][1] - p[0][1]) * cx - (p[1][0] - p[0][0]) * cy + p[1][0] * p[0][1] - p[1][1] * p[0][0]) / \
                np.sqrt((p[1][1] - p[0][1]) ** 2 + (p[1][0] - p[0][0]) ** 2)
            if d <= radius:
                score += 1
    return score
