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
import matlab.engine


def traj_matlab(x, nx):
    tx = matlab.double(np.reshape(x[0:nx], (1, nx))[0].tolist())
    ty = matlab.double(np.reshape(x[nx:], (1, nx))[0].tolist())
    x_matlab = eng.trajectory_following(tx, ty)
    return np.hstack(((x_matlab[0]), x_matlab[1]))


eng = matlab.engine.start_matlab()

traj0 = [(0, 0), (0.08, 0.06),  (0.24, 0.15), (0.31, 0.21),  (0.41, 0.3), (0.47, 0.36),
        (0.54, 0.43), (0.65, 0.55), (0.72, 0.62), (0.8, 0.7), (0.85, 0.77), (0.87, 0.81),
        (0.94, 0.91), (0.98, 0.98), (1, 1)]
traj0 = np.transpose(np.array(traj0) * 20)

obstacle = {1: [(7, 4), (9, 4), (9, 6), (7, 6)],
            2: [(10, 12), (12, 12), (12, 14), (10, 14)]}

do_local_perturb = 1
both = 1
# zero-order parameter
max_period = 50
max_itr = int(sys.argv[1])

eta = 1e-1  # Note: step size rule 1 does not work well when dimension is larger than 2  1e-2
delta = 1e1  # exploration parameter

nx = np.shape(traj0)[1]

if not do_local_perturb or both:
    # container
    x_period = np.zeros((nx * 2, max_period))
    human_period = {k: [] for k in range(max_period)}
    complaint_period = np.zeros((max_itr+1, max_period))
    acc_regret = np.zeros((max_itr+1, max_period))
    traj = list(traj0)
if do_local_perturb or both:
    # container
    x_period1 = np.zeros((nx * 2, max_period))
    human_period1 = {k: [] for k in range(max_period)}
    complaint_period1 = np.zeros((max_itr+1, max_period))
    acc_regret1 = np.zeros((max_itr+1, max_period))
    traj1 = list(traj0)

human, human_scale = get_cluster(obstacle)

for t in tqdm(range(max_period)):
    if not do_local_perturb or both:
        # inner iteraions within one period
        xt = np.zeros((nx * 2, max_itr+1))
        xt[:, 0] = np.reshape(traj, (nx * 2, 1), order='C').ravel()
        dist0 = 0
        eta = 1e-1
        succ = False
        for i in range(max_itr):

            x = np.reshape(xt[:, i], (nx * 2, 1))
            x_matlab = traj_matlab(x, nx)
            s, complaint, dist, index = human_feedback1(xt[:, i], x_matlab, human, obstacle, human_scale)
            # collect complaint
            complaint_period[i][t] = complaint
            # print(i, s - dist, dist)
            if s - dist < 1e-2:
                succ = True
                break
            dist0 = dist
            ut = np.random.random((nx * 2, 1)) * 2 - 1
            # keep the start and end still
            ut[0] = 0
            ut[nx - 1] = 0
            ut[nx] = 0
            ut[-1] = 0
            ut = ut / np.linalg.norm(ut)

            # call matlab then get bandit human feedback
            x_plus = x + ut * delta
            x_plus_matlab = traj_matlab(x_plus, nx)
            s_plus, _, _, _ = human_feedback1(x_plus.ravel(), x_plus_matlab, human, obstacle, human_scale)
            # call matlab then get bandit human feedback
            x_minus = x - ut * delta
            x_minus_matlab = traj_matlab(x_minus, nx)
            s_minus, _, _, _ = human_feedback1(x_minus.ravel(), x_minus_matlab, human, obstacle, human_scale)

            gt = nx * 2 / 2 / delta * (s_plus - s_minus) * ut  # gradient
            xt[:, i + 1] = xt[:, i] - eta * gt.ravel()  # gradient descent

        if not succ:
            x = np.reshape(xt[:, i+1], (nx * 2, 1))
            x_matlab = traj_matlab(x, nx)
            s, complaint, dist, index = human_feedback1(xt[:, i+1], x_matlab, human, obstacle, human_scale)
            complaint_period[i+1][t] = complaint

        # initial traj for the next period
        traj = x_matlab
        # print('full', t, i)
        x_period[:, t] = x_matlab
        human_period[t] = human

        # x = np.reshape(xt[:, i], (nx * 2, 1))
        # workspace_plot(x, nx, human_cluster, obstacle, meas, human)
        # plt.show()

    if do_local_perturb or both:
        # inner iteraions within one period
        eta1 = 5e-1
        xt1 = np.zeros((nx * 2, max_itr+1))
        xt1[:, 0] = np.reshape(traj1, (nx * 2, 1), order='C').ravel()
        dist0 = 0
        succ = False
        # inner iterations within one period
        for i in range(max_itr):
            x = np.reshape(xt1[:, i], (nx * 2, 1))
            x_matlab = traj_matlab(x, nx)  # do not use motion planner path
            s,  complaint, dist, index = human_feedback1(xt1[:, i], x_matlab, human, obstacle, human_scale)
            # print(i, s - dist, dist)
            complaint_period1[i][t] = complaint

            if s - dist < 1e-2:
                succ = True
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
            # call matlab then get bandit human feedback
            x_plus = x + ut * delta
            x_plus_matlab = traj_matlab(x_plus, nx)
            s_plus, _, _, _ = human_feedback1(x_plus.ravel(), x_plus_matlab, human, obstacle, human_scale)
            # call matlab then get bandit human feedback
            x_minus = x - ut * delta
            x_minus_matlab = traj_matlab(x_minus, nx)
            s_minus, _, _, _ = human_feedback1(x_minus.ravel(), x_minus_matlab, human, obstacle, human_scale)

            gt = np.count_nonzero(ut) / 2 / delta * (s_plus - s_minus) * ut  # gradient
            xt1[:, i + 1] = xt1[:, i] - eta1 * gt.ravel()  # gradient descent

        if not succ:
            x = np.reshape(xt1[:, i + 1], (nx * 2, 1))
            x_matlab = traj_matlab(x, nx)
            s, complaint, dist, index = human_feedback1(xt1[:, i + 1], x_matlab, human, obstacle, human_scale)
            complaint_period1[i + 1][t] = complaint
        # initial traj for the next period
        traj1 = x_matlab
        # print('local', t, i)
        x_period1[:, t] = x_matlab
        human_period1[t] = human

    # update human position
    human, human_scale = update_cluster(human, obstacle)

# calculate accumulative regret
if not do_local_perturb or both:
    for i in range(max_period):
        acc_regret[:, i] = acc_regret[:, i - 1] + complaint_period[:, i] if i > 0 else complaint_period[:, i]

if do_local_perturb or both:
    for i in range(max_period):
        acc_regret1[:, i] = acc_regret1[:, i - 1] + complaint_period1[:, i] if i > 0 else complaint_period1[:, i]

    # visualization
    # vis(human_cluster, obstacle, human_period1, x_period1, complaint_period1, human_scale)
    # regret_plot(acc_regret1)

# max_itr_radius_repeat
with open('data/{0}_{1}_{2}'.format(int(sys.argv[1]), int(float(sys.argv[2])*10), int(sys.argv[3])), 'wb') as filehandle:
    pickle.dump(acc_regret, filehandle)
    pickle.dump(acc_regret1, filehandle)

# plt.show()
# plt.legend()