from workspace import Workspace
import matplotlib.pyplot as plt
import pickle
from draw_workspace import workspace_plot
import numpy as np
from human_feedback import human_feedback1
from generate_cluster import get_cluster, update_cluster
import sys
import warnings
from vis import vis, regret_plot
from tqdm import tqdm


traj0 = [(0.3, 0), (0.34, 0.09), (0.35, 0.19), (0.37, 0.29), (0.39, 0.33), (0.41, 0.42),
        (0.44, 0.51), (0.46, 0.57), (0.5, 0.65), (0.57, 0.73), (0.61, 0.78), (0.67, 0.86),
        (1, 1)]
traj0 = np.transpose(np.array(traj0) * 20)

human_cluster = {1: [(5, 5), (8, 3), (9, 3), (9, 4), (7, 7), (5, 7)],
                 2: [(13, 5), (15, 1), (16, 1), (16, 4), (14, 6), (13, 6)],
                 3: [(14, 8), (18, 8), (18, 10), (14, 10)],
                 4: [(10, 12), (11, 12), (14, 13), (14, 14), (11, 16), (10, 16)],
                 5: [(5, 13), (6, 13), (6, 16), (3, 17), (2, 17), (2, 15)]}
# obstacle = {1: [(9, 9), (11, 9), (11, 11), (9, 11)]}
obstacle = {1: [(10.5, 9), (12.5, 9), (12.5, 11), (10.5, 11)],
            2: [(4, 9), (6, 9), (6, 11), (4, 11)]}

human, point_cluster, human_scale = get_cluster(obstacle)
do_local_perturb = 1
both = 1
# zero-order parameter
max_period = 100
max_itr = int(sys.argv[1])

eta = 1e-1  # Note: step size rule 1 does not work well when dimension is larger than 2  1e-2
delta = 1e1  # exploration parameter

nx = np.shape(traj0)[1]

if not do_local_perturb or both:
    # container
    x_period = np.zeros((nx * 2, max_period))
    human_period = {k: [] for k in range(max_period)}
    complaint_period = []
    acc_regret = np.zeros((1, max_period)).ravel()
    traj = list(traj0)
if do_local_perturb or both:
    # container
    x_period1 = np.zeros((nx * 2, max_period))
    human_period1 = {k: [] for k in range(max_period)}
    complaint_period1 = []
    acc_regret1 = np.zeros((1, max_period)).ravel()
    traj1 = list(traj0)

for t in tqdm(range(max_period)):
    if not do_local_perturb or both:
        # inner iteraions within one period
        xt = np.zeros((nx * 2, max_itr))
        xt[:, 0] = np.reshape(traj, (nx * 2, 1), order='C').ravel()
        dist0 = 0
        for i in range(max_itr - 1):
            x = np.reshape(xt[:, i], (nx * 2, 1))
            # s, dist, index = human_feedback(x, human_cluster, point_cluster, obstacle)
            s, complaint, dist, index = human_feedback1(x, human, obstacle, human_scale)
            # print(i, s - dist, dist)
            if np.fabs(dist - dist0) < 1 and s - dist < 1e-2:
                break
            dist0 = dist
            ut = np.random.random((nx * 2, 1)) * 2 - 1
            # keep the start and end still
            ut[0] = 0
            ut[nx - 1] = 0
            ut[nx] = 0
            ut[-1] = 0
            ut = ut / np.linalg.norm(ut)

            x_plus = x + ut * delta
            # s_plus, _, _ = human_feedback(x_plus, human_cluster, point_cluster, obstacle)
            s_plus, _, _, _ = human_feedback1(x_plus, human, obstacle, human_scale)

            x_minus = x - ut * delta
            # s_minus, _, _ = human_feedback(x_minus, human_cluster, point_cluster, obstacle)
            s_minus, _, _, _ = human_feedback1(x_minus, human, obstacle, human_scale)

            gt = nx * 2 / 2 / delta * (s_plus - s_minus) * ut  # gradient

            xt[:, i + 1] = xt[:, i] - eta * gt.ravel()  # gradient descent

        # initial traj for the next period
        traj = xt[:, i]
        # print('full', t, i)
        x_period[:, t] = xt[:, i]
        human_period[t] = human
        complaint_period.append(complaint)

        # x = np.reshape(xt[:, i], (nx * 2, 1))
        # workspace_plot(x, nx, human_cluster, obstacle, meas, human)
        # plt.show()

    if do_local_perturb or both:
        # inner iteraions within one period
        xt1 = np.zeros((nx * 2, max_itr))
        xt1[:, 0] = np.reshape(traj1, (nx * 2, 1), order='C').ravel()
        dist0 = 0
        # inner iterations within one period
        for i in range(max_itr - 1):
            x = np.reshape(xt1[:, i], (nx * 2, 1))
            s,  complaint, dist, index = human_feedback1(x, human, obstacle, human_scale)
            # print(i, s - dist, dist)
            if np.fabs(dist - dist0) < 1 and s - dist < 1e-2:
                break
            dist0 = dist
            ut = np.random.random((nx * 2, 1)) * 2 - 1
            # local perturb
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
                except Warning:
                    # in case all entries of ut are 0's
                    ut = np.random.random((nx * 2, 1))
                    ut[0] = 0
                    ut[nx - 1] = 0
                    ut[nx] = 0
                    ut[-1] = 0
                    ut = ut / np.linalg.norm(ut)

            x_plus = x + ut * delta
            s_plus, _, _, _ = human_feedback1(x_plus, human, obstacle, human_scale)
            x_minus = x - ut * delta
            s_minus, _, _, _ = human_feedback1(x_minus, human, obstacle, human_scale)

            gt = nx * 2 / 2 / delta * (s_plus - s_minus) * ut  # gradient

            xt1[:, i + 1] = xt1[:, i] - eta * gt.ravel()  # gradient descent

        # initial traj for the next period
        traj1 = xt1[:, i]
        # print('local', t, i)
        x_period1[:, t] = xt1[:, i]
        human_period1[t] = human
        complaint_period1.append(complaint)

    # update human position
    human, human_scale = update_cluster(human)

# calculate accumulative regret
if not do_local_perturb or both:
    for i in range(len(complaint_period)):
        acc_regret[i] = acc_regret[i - 1] + complaint_period[i] if i > 0 else complaint_period[i]

    # visualization
    # vis(human_cluster, obstacle, human_period, x_period, complaint_period, human_scale)
    # regret_plot(acc_regret)

if do_local_perturb or both:
    for i in range(len(complaint_period1)):
        acc_regret1[i] = acc_regret1[i - 1] + complaint_period1[i] if i > 0 else complaint_period1[i]

    # visualization
    # vis(human_cluster, obstacle, human_period1, x_period1, complaint_period1, human_scale)
    # regret_plot(acc_regret1)

# max_itr_radius_repeat
with open('data/{0}_{1}_{2}'.format(int(sys.argv[1]), int(float(sys.argv[2])*10), int(sys.argv[3])), 'wb') as filehandle:
    pickle.dump(acc_regret, filehandle)
    pickle.dump(acc_regret1, filehandle)

# plt.show()
# plt.legend()