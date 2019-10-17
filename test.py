# # import matplotlib
# import numpy as np
# import matplotlib.pyplot as plt
# import pickle
# import random
# # from matplotlib.patches import Polygon
# # from matplotlib.collections import PatchCollection
# # fig = plt.figure()
# # axe = fig.add_subplot(111)
# # polyval = numpy.random.rand(4,2) # Create the sequence of 4 2D points
# # patches = [Polygon(polyval,True)]
# # p = PatchCollection(patches,cmap=matplotlib.cm.jet,alpha=0.3)
# # p.set_array(100.*numpy.random.rand(1)) # Set a random color on jet map
# # axe.add_collection(p)
# # fig.colorbar(p)
# # fig.show()
# # for patch in patches:
# #    axe.add_patch(Polygon(patch.get_xy(),closed=True,ec='k',lw=3,fill=False)) #draw the contours
# # fig.canvas.draw()
# # plt.show()
#
# plt.rc('text', usetex=True)
# plt.rc('font', family='serif')
# # plt.gca().set_aspect('equal', adjustable='box')
# plt.grid(b=True, which='major', color='k', linestyle='--')
# max_period = 4
# repeat = 2
# for i in [10, 20, 30]:
#     for j in [3, 5, 10]:
#         regret = np.zeros((1, max_period)).ravel()
#         regret1 = np.zeros((1, max_period)).ravel()
#         for k in range(1, repeat+1):
#             with open('data/{0}_{1}_{2}'.format(i, j, k), 'rb') as filehandle:
#                 acc_regret = pickle.load(filehandle)
#                 acc_regret1 = pickle.load(filehandle)
#                 regret += acc_regret
#                 regret1 += acc_regret1
#         regret = regret / repeat
#         regret1 = regret1 / repeat
#         c = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
#         plt.plot(list(range(max_period)), regret, '--', color=c)
#         plt.plot(list(range(max_period)), regret1, '-', color=c)
#
# plt.show()

# import matlab.engine
# import numpy as np
# x0 = np.array([1, 0, 3])
# eng = matlab.engine.start_matlab()
# x = matlab.double(np.array(x0).tolist())


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


# traj and cluster
# traj = [(0.3, 0), (0.34, 0.09), (0.35, 0.19), (0.37, 0.29), (0.39, 0.33), (0.41, 0.42),
#         (0.44, 0.51), (0.46, 0.57), (0.5, 0.65), (0.57, 0.73), (0.61, 0.78), (0.67, 0.86),
#         (1, 1)]
# traj = [(0, 0), (0.08, 0.06), (0.17, 0.11), (0.24, 0.15), (0.31, 0.21), (0.38, 0.27), (0.41, 0.3), (0.47, 0.36),
#         (0.54, 0.43), (0.58, 0.48), (0.65, 0.55), (0.72, 0.62), (0.75, 0.65), (0.8, 0.7), (0.85, 0.77), (0.87, 0.81),
#         (0.9, 0.86), (0.94, 0.91), (0.98, 0.98), (1, 1)]

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

obstacle = {1: [(10.5, 9), (12.5, 9), (12.5, 11), (10.5, 11)],
            }
# 2: [(4, 9), (6, 9), (6, 11), (4, 11)]

# obstacle = {}
# a = {'1': (4, 4), '2': (14, 4), '3': (4, 14), '4': (14, 14)}
# for k, v in a.items():
#     obstacle[k] = ([(v[0], v[1]), ((v[0]+2), v[1]), ((v[0]+2), (v[1]+2)), (v[0], (v[1]+2))])

human, human_scale = get_cluster(human_cluster)
do_local_perturb = 1
both = 0
# zero-order parameter
maxItr = int(1e4)
eta = 1e-2  # Note: step size rule 1 does not work well when dimension is larger than 2  1e-2
delta = 1e1  # exploration parameter

nx = np.shape(traj)[1]

if do_local_perturb or both:
    xt = np.zeros((nx * 2, maxItr))
    xt[:, 0] = np.reshape(traj, (nx * 2, 1), order='C').ravel()
    meas = np.zeros((maxItr,))  # Distance me
    dist0 = 0
    for i in range(maxItr - 1):
        print(i)
        x = np.reshape(xt[:, i], (nx * 2, 1))
        tx = matlab.double(np.reshape(x[0:nx], (1, nx))[0].tolist())
        ty = matlab.double(np.reshape(x[nx:], (1, nx))[0].tolist())
        x = eng.trajectory_following(tx, ty)
        x = np.hstack(((x[0]), x[1]))
        s, _, dist, index = human_feedback1(x, human, obstacle, human_scale)
        meas[i] = s

eng.quit()
