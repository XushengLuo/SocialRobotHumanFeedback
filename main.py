from workspace import Workspace
import matplotlib.pyplot as plt
import pickle
from draw_workspace import workspace_plot
import numpy as np
from human_feedback import human_feedback1
from generate_cluster import get_cluster, update_cluster
import sys
import warnings
from shapely.geometry import Polygon
from tqdm import tqdm
import matlab.engine
# from python to call matlab: https://github.com/byuflowlab/pyfmincon


def traj_matlab(x, nx):
    tx = matlab.double(np.reshape(x[0:nx], (1, nx))[0].tolist())
    ty = matlab.double(np.reshape(x[nx:], (1, nx))[0].tolist())
    x_matlab = eng.trajectory_following(tx, ty)
    return np.hstack(((x_matlab[0]), x_matlab[1]))


eng = matlab.engine.start_matlab()

traj = [(0, 0), (0.08, 0.06),  (0.24, 0.15), (0.31, 0.21),  (0.41, 0.3), (0.47, 0.36),
        (0.54, 0.43), (0.65, 0.55), (0.72, 0.62), (0.8, 0.7), (0.85, 0.77), (0.87, 0.81),
        (0.94, 0.91), (0.98, 0.98), (1, 1)]
traj = np.transpose(np.array(traj) * 20)

obstacle = {1: [(7, 4), (9, 4), (9, 6), (7, 6)],
            2: [(10, 12), (12, 12), (12, 14), (10, 14)]}

# traj = [(0, 0), (0.08, 0.07), (0.15, 0.13), (0.23, 0.2), (0.3, 0.26), (0.38, 0.33),
#         (0.45, 0.4), (0.53, 0.46), (0.6, 0.52), (0.63, 0.55), (0.67, 0.59), (0.74, 0.65), (0.78, 0.68), (0.85, 0.75),
#         (0.87, 0.8), (0.84, 0.82), (0.76, 0.87), (0.71, 0.87), (0.61, 0.87), (0.51, 0.88)]
#
# traj = np.transpose(np.array(traj) * 20)
#
# # challenginng obstacles
# obs = {3: [(8, 19), (17, 19), (17, 20), (8, 20)],
#        4: [(8, 16), (9, 16), (9, 19), (8, 19)],
#        5: [(8, 15), (17, 15), (17, 16), (8, 16)]}
#
# obs = {3: [(8, 19), (12, 19), (12, 20), (8, 20)],
#        4: [(8, 16), (9, 16), (9, 19), (8, 19)],
#        5: [(8, 15), (12, 15), (12, 16), (8, 16)]}
# obstacle.update(obs)

do_local_perturb = 1
both = 0
# zero-order parameter
maxItr = 100
delta = 1e1  # exploration parameter

nx = np.shape(traj)[1]
full = None
for ii in (range(1)):   # number of updates of human positions
    human, human_scale = get_cluster(obstacle)
    # with open('data/human', 'wb') as filehandle:
    #     pickle.dump(human, filehandle)
    #     pickle.dump(human_scale, filehandle)
    # with open('data/human', 'rb') as filehandle:
    #     human = pickle.load(filehandle)
    #     human_scale = pickle.load(filehandle)
    # full perturb
    if not do_local_perturb or both:
        eta = 1e-1
        xt = np.zeros((nx * 2, maxItr))
        xt[:, 0] = np.reshape(traj, (nx * 2, 1), order='C').ravel()
        meas = np.zeros((maxItr,))  # Distance me
        dist0 = 0
        for i in (range(maxItr - 1)):
            # call matlab then get bandit human feedback
            x = np.reshape(xt[:, i], (nx * 2, 1))
            x_matlab = traj_matlab(x, nx)
            s, _, dist, _ = human_feedback1(xt[:, i], x_matlab, human, obstacle, human_scale)
            meas[i] = s
            print(i, (s - dist)/10)
            if s - dist < 1e-2:  # np.fabs(dist - dist0) < 1 and
                full = x_matlab
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
            # if i % 5 == 0 and i != 0:
            #     path = {'x': x, 'x_m': x_matlab}
            #     workspace_plot(path, nx, obstacle, meas, human, human_scale)
            #     plt.draw()
            #     plt.pause(10)
        dist = np.sum([np.linalg.norm([x_matlab[i] - x_matlab[i + 1], x_matlab[i + nx] - x_matlab[i + 1 + nx]])
                       for i in range(nx - 1)])
        print(i, dist, end=', ')

    # local perturb
    if do_local_perturb or both:
        eta1 = 5e-1
        xt = np.zeros((nx * 2, maxItr))
        xt[:, 0] = np.reshape(traj, (nx * 2, 1), order='C').ravel()
        meas = np.zeros((maxItr,))  # Distance me
        dist0 = 0
        for i in (range(maxItr - 1)):
            # call matlab then get bandit human feedback
            x = np.reshape(xt[:, i], (nx * 2, 1))
            x_matlab = traj_matlab(x, nx)  # do not use motion planner path
            s, _, dist, index = human_feedback1(xt[:, i], x_matlab, human, obstacle, human_scale)
            meas[i] = s
            print(i, (s - dist)/10, index)
            if s - dist < 1e-2:  # np.fabs(dist - dist0) < 1 and
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
            # print(eta * np.transpose(gt))
            xt[:, i + 1] = xt[:, i] - eta1 * gt.ravel()  # gradient descent
            # if i % 1 == 0:
            #     path = {'x': x, 'x_m': x_matlab}
            #     workspace_plot(path, nx, obstacle, meas, human, human_scale)
            #     plt.draw()
            #     plt.pause(10)
        dist = np.sum([np.linalg.norm([x_matlab[i] - x_matlab[i + 1], x_matlab[i + nx] - x_matlab[i + 1 + nx]])
                       for i in range(nx - 1)])
        print(i, dist, end=',')
    path = {r'$\mathbf{x}_0$': np.reshape(traj, (nx * 2, 1), order='C').ravel(),
            r'$\mathbf{x}_{\mathrm{zero}}$': x, r'$\mathbf{x}_{\mathrm{MPC}}$': x_matlab}
    workspace_plot(path, nx, obstacle, meas, human, human_scale)
    plt.savefig('/Users/chrislaw/Box Sync/Research/Zero_Opt2019/fig/demo.pdf', format="pdf")
    plt.show()
    print('')
eng.quit()
# x = np.reshape(xt[:, i], (nx * 2, 1))
# workspace_plot(x, nx, obstacle, meas, human, human_scale)

# plt.show()


