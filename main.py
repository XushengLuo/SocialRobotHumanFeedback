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
import matlab.engine
# from python to call matlab: https://github.com/byuflowlab/pyfmincon

# traj and cluster
# traj = [(0.3, 0), (0.34, 0.09), (0.35, 0.19), (0.37, 0.29), (0.39, 0.33), (0.41, 0.42),
#         (0.44, 0.51), (0.46, 0.57), (0.5, 0.65), (0.57, 0.73), (0.61, 0.78), (0.67, 0.86),
#         (1, 1)]
# traj = [(0, 0), (0.08, 0.06), (0.17, 0.11), (0.24, 0.15), (0.31, 0.21), (0.38, 0.27), (0.41, 0.3), (0.47, 0.36),
#         (0.54, 0.43), (0.58, 0.48), (0.65, 0.55), (0.72, 0.62), (0.75, 0.65), (0.8, 0.7), (0.85, 0.77), (0.87, 0.81),
#         (0.9, 0.86), (0.94, 0.91), (0.98, 0.98), (1, 1)]


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

human_cluster = {1: [(5, 5), (8, 3), (9, 3), (9, 4), (7, 7), (5, 7)],
                 2: [(13, 5), (15, 1), (16, 1), (16, 4), (14, 6), (13, 6)],
                 3: [(14, 8), (18, 8), (18, 10), (14, 10)],
                 4: [(10, 12), (11, 12), (14, 13), (14, 14), (11, 16), (10, 16)],
                 5: [(5, 13), (6, 13), (6, 16), (3, 17), (2, 17), (2, 15)]}

# obstacle = {1: [(10.5, 9), (12.5, 9), (12.5, 11), (10.5, 11)],
#             }
obstacle = {1: [(7, 4), (9, 4), (9, 6), (7, 6)],
            2: [(10, 12), (12, 12), (12, 14), (10, 14)]}

do_local_perturb = 1
both = 0
# zero-order parameter
maxItr = int(1e4)
eta = 1e-1  # Note: step size rule 1 does not work well when dimension is larger than 2  1e-2
delta = 1e1  # exploration parameter

nx = np.shape(traj)[1]

for ii in range(4):   # number of updates of human positions
    human, human_scale = get_cluster(human_cluster)
    # full perturb
    if not do_local_perturb or both:
        xt = np.zeros((nx * 2, maxItr))
        xt[:, 0] = np.reshape(traj, (nx * 2, 1), order='C').ravel()
        meas = np.zeros((maxItr,))  # Distance me
        dist0 = 0
        for i in range(maxItr - 1):
            # call matlab
            x = np.reshape(xt[:, i], (nx * 2, 1))
            tx = matlab.double(np.reshape(x[0:nx], (1, nx))[0].tolist())
            ty = matlab.double(np.reshape(x[nx:], (1, nx))[0].tolist())
            x_matlab = eng.trajectory_following(tx, ty)
            x_matlab = np.hstack(((x_matlab[0]), x_matlab[1]))
            # bandit human feedback
            s, _, dist, _ = human_feedback1(x_matlab, human, obstacle, human_scale)
            meas[i] = s
            # print(i, s - dist, dist)
            if s - dist < 1e-2:  # np.fabs(dist - dist0) < 1 and
                break
            dist0 = dist
            ut = np.random.random((nx * 2, 1)) * 2 - 1
            # keep the start and end still
            ut[0] = 0
            ut[nx - 1] = 0
            ut[nx] = 0
            ut[-1] = 0
            ut = ut / np.linalg.norm(ut)

            # call matlab
            x_plus = x + ut * delta
            tx = matlab.double(np.reshape(x_plus[0:nx], (1, nx))[0].tolist())
            ty = matlab.double(np.reshape(x_plus[nx:], (1, nx))[0].tolist())
            x_plus_matlab = eng.trajectory_following(tx, ty)
            x_plus_matlab = np.hstack(((x_plus_matlab[0]), x_plus_matlab[1]))
            s_plus, _, _, _ = human_feedback1(x_plus_matlab, human, obstacle, human_scale)
            # call matlab
            x_minus = x - ut * delta
            tx = matlab.double(np.reshape(x_minus[0:nx], (1, nx))[0].tolist())
            ty = matlab.double(np.reshape(x_minus[nx:], (1, nx))[0].tolist())
            x_minus_matlab = eng.trajectory_following(tx, ty)
            x_minus_matlab = np.hstack(((x_minus_matlab[0]), x_minus_matlab[1]))
            s_minus, _, _, _ = human_feedback1(x_minus_matlab, human, obstacle, human_scale)

            gt = nx * 2 / 2 / delta * (s_plus - s_minus) * ut  # gradient
            xt[:, i + 1] = xt[:, i] - eta * gt.ravel()  # gradient descent
            # path = {'x': x, 'x_m': x_matlab, 'xp': x_plus, 'xp_m': x_plus_matlab, 'xm': x_minus, 'xm_m': x_minus_matlab}
            path = {'x': x, 'x_m': x_matlab}
            workspace_plot(path, nx, obstacle, meas, human, human_scale)
            plt.draw()
            plt.pause(10)
        print(i, end=', ')

    # local perturb
    if do_local_perturb or both:
        xt = np.zeros((nx * 2, maxItr))
        xt[:, 0] = np.reshape(traj, (nx * 2, 1), order='C').ravel()
        meas = np.zeros((maxItr,))  # Distance me
        dist0 = 0
        for i in range(maxItr - 1):
            # call matlab
            x = np.reshape(xt[:, i], (nx * 2, 1))
            x_matlab = traj_matlab(x, nx)
            # tx = matlab.double(np.reshape(x[0:nx], (1, nx))[0].tolist())
            # ty = matlab.double(np.reshape(x[nx:], (1, nx))[0].tolist())
            # x_matlab = eng.trajectory_following(tx, ty)
            # x_matlab = np.hstack(((x_matlab[0]), x_matlab[1]))
            # bandit human feedback
            s, _, dist, index = human_feedback1(x_matlab, human, obstacle, human_scale)
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
            # call matlab
            x_plus = x + ut * delta
            x_plus_matlab = traj_matlab(x_plus, nx)
            # tx = matlab.double(np.reshape(x_plus[0:nx], (1, nx))[0].tolist())
            # ty = matlab.double(np.reshape(x_plus[nx:], (1, nx))[0].tolist())
            # x_plus_matlab = eng.trajectory_following(tx, ty)
            # x_plus_matlab = np.hstack(((x_plus_matlab[0]), x_plus_matlab[1]))
            s_plus, _, _, _ = human_feedback1(x_plus_matlab, human, obstacle, human_scale)
            # call matlab
            x_minus = x - ut * delta
            x_minus_matlab = traj_matlab(x_minus, nx)
            # tx = matlab.double(np.reshape(x_minus[0:nx], (1, nx))[0].tolist())
            # ty = matlab.double(np.reshape(x_minus[nx:], (1, nx))[0].tolist())
            # x_minus_matlab = eng.trajectory_following(tx, ty)
            # x_minus_matlab = np.hstack(((x_minus_matlab[0]), x_minus_matlab[1]))
            s_minus, _, _, _ = human_feedback1(x_minus_matlab, human, obstacle, human_scale)

            gt = nx * 2 / 2 / delta * (s_plus - s_minus) * ut  # gradient
            xt[:, i + 1] = xt[:, i] - eta * gt.ravel()  # gradient descent

            # path = {'x': x, 'x_m': x_matlab, 'xp': x_plus, 'xp_m': x_plus_matlab, 'xm': x_minus, 'xm_m': x_minus_matlab}
            path = {'x': x, 'x_m': x_matlab}
            workspace_plot(path, nx, obstacle, meas, human, human_scale)
            plt.draw()
            plt.pause(10)
        print(i, end=',')

        x = np.reshape(xt[:, i], (nx * 2, 1))
        tx = matlab.double(np.reshape(x[0:nx], (1, nx))[0].tolist())
        ty = matlab.double(np.reshape(x[nx:], (1, nx))[0].tolist())
        x_matlab = eng.trajectory_following(tx, ty)
        x_matlab = np.hstack(((x_matlab[0]), x_matlab[1]))
        path = {'x': x, 'x_m': x_matlab}
        workspace_plot(path, nx, obstacle, meas, human, human_scale)
        plt.show()

print('')
eng.quit()
# x = np.reshape(xt[:, i], (nx * 2, 1))
# workspace_plot(x, nx, obstacle, meas, human, human_scale)

# plt.show()


