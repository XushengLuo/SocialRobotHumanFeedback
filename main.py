from workspace import Workspace
import matplotlib.pyplot as plt
import pickle
from draw_workspace import workspace_plot
import numpy as np
from human_feedback import human_feedback
from generate_cluster import get_cluster
import sys
import warnings


traj0 = [(0.3, 0), (0.34, 0.09), (0.35, 0.19), (0.37, 0.29), (0.39, 0.33), (0.41, 0.42),
        (0.44, 0.51), (0.46, 0.57), (0.5, 0.65), (0.57, 0.73), (0.61, 0.78), (0.67, 0.86),
        (1, 1)]
traj = []
for i in range(len(traj0)-1):
    traj.append(traj0[i])
    traj.append(((traj0[i+1][0]+traj0[i][0])/2, (traj0[i+1][1]+traj0[i][1])/2))
traj.append(traj0[-1])
# (0.67, 0.86) 0.875, 0.625
# traj and cluster
traj = np.transpose(np.array(traj) * 20)

human_cluster = {1: [(5, 5), (8, 3), (9, 3), (9, 4), (7, 7), (5, 7)],
                 2: [(13, 5), (15, 1), (16, 1), (16, 4), (14, 6), (13, 6)],
                 3: [(14, 9), (18, 9), (18, 10), (14, 10)],
                 4: [(10, 12), (11, 12), (14, 13), (14, 14), (11, 16), (10, 16)],
                 5: [(5, 13), (6, 13), (6, 16), (3, 17), (2, 17), (2, 15)]}
obstacle = {1: [(9, 9), (11, 9), (11, 11), (9, 11)]}
# obstacle = {1: [(10.5, 9), (12.5, 9), (12.5, 11), (10.5, 11)]}

human, point_cluster = get_cluster(human_cluster)
do_local_perturb = int(sys.argv[1])
# zero-order parameter
maxItr = int(1e4)
eta = 1e-1  # Note: step size rule 1 does not work well when dimension is larger than 2  1e-2
delta = 1e1  # exploration parameter

nx = np.shape(traj)[1]

if not do_local_perturb:
    xt = np.zeros((nx * 2, maxItr))
    xt[:, 0] = np.reshape(traj, (nx * 2, 1), order='C').ravel()
    meas = np.zeros((maxItr,))  # Distance me
    dist0 = 0
    for i in range(maxItr - 1):
        x = np.reshape(xt[:, i], (nx * 2, 1))
        s, dist, index = human_feedback(x, human_cluster, point_cluster, obstacle)
        meas[i] = s
        # print(i, s - dist, dist)
        if np.fabs(dist - dist0) < 1 and s - dist < 1e-2:
            break
        dist0 = dist
        ut = np.random.random((nx * 2, 1))
        # keep the start and end still
        ut[0] = 0
        ut[nx - 1] = 0
        ut[nx] = 0
        ut[-1] = 0

        x_plus = x + ut * delta
        s_plus, _, _ = human_feedback(x_plus, human_cluster, point_cluster, obstacle)
        x_minus = x - ut * delta
        s_minus, _, _ = human_feedback(x_minus, human_cluster, point_cluster, obstacle)

        gt = nx * 2 / 2 / delta * (s_plus - s_minus) * ut  # gradient

        xt[:, i + 1] = xt[:, i] - eta * gt.ravel()  # gradient descent
    print(i)
elif do_local_perturb:
    xt = np.zeros((nx * 2, maxItr))
    xt[:, 0] = np.reshape(traj, (nx * 2, 1), order='C').ravel()
    meas = np.zeros((maxItr,))  # Distance me
    dist0 = 0
    for i in range(maxItr - 1):
        x = np.reshape(xt[:, i], (nx * 2, 1))
        s, dist, index = human_feedback(x, human_cluster, point_cluster, obstacle)
        meas[i] = s
        # print(i, s - dist, dist)
        if np.fabs(dist - dist0) < 1 and s - dist < 1e-2:
            break
        dist0 = dist
        ut = np.random.random((nx * 2, 1))
        # local perturb
        if do_local_perturb:
            for j in range(1, nx):
                if j not in index:
                    ut[j] = 0
                    ut[j + nx] = 0
        # keep the start and end still
        ut[0] = 0
        ut[nx - 1] = 0
        ut[nx] = 0
        ut[-1] = 0
        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                ut = ut / np.linalg.norm(ut)
            except Warning as e:
                # in case all entries of ut are 0's
                ut = np.random.random((nx * 2, 1))
                ut[0] = 0
                ut[nx - 1] = 0
                ut[nx] = 0
                ut[-1] = 0
                ut = ut / np.linalg.norm(ut)

        x_plus = x + ut * delta
        s_plus, _, _ = human_feedback(x_plus, human_cluster, point_cluster, obstacle)
        x_minus = x - ut * delta
        s_minus, _, _ = human_feedback(x_minus, human_cluster, point_cluster, obstacle)

        gt = nx * 2 / 2 / delta * (s_plus - s_minus) * ut  # gradient

        xt[:, i + 1] = xt[:, i] - eta * gt.ravel()  # gradient descent

    print(i)
# x = np.reshape(xt[:, i], (nx * 2, 1))
# workspace_plot(x, nx, human_cluster, obstacle, meas, human)
#
# plt.show()

