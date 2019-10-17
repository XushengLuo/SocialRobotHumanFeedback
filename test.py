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

import matlab.engine
import numpy as np
x0 = np.array([1, 0, 3])
eng = matlab.engine.start_matlab()
x = matlab.double(np.array(x0).tolist())
eng.quit()
