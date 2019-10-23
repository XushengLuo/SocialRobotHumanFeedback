# import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pickle
import random
# from matplotlib.patches import Polygon
# from matplotlib.collections import PatchCollection
# fig = plt.figure()
# axe = fig.add_subplot(111)
# polyval = numpy.random.rand(4,2) # Create the sequence of 4 2D points
# patches = [Polygon(polyval,True)]
# p = PatchCollection(patches,cmap=matplotlib.cm.jet,alpha=0.3)
# p.set_array(100.*numpy.random.rand(1)) # Set a random color on jet map
# axe.add_collection(p)
# fig.colorbar(p)
# fig.show()
# for patch in patches:
#    axe.add_patch(Polygon(patch.get_xy(),closed=True,ec='k',lw=3,fill=False)) #draw the contours
# fig.canvas.draw()
# plt.show()
fig = plt.figure()
ax = fig.add_subplot(111)
plt.rc('font', family='serif')
plt.rc('text', usetex=True)
# plt.gca().set_aspect('equal', adjustable='box')
plt.grid(b=True, which='major', color='gray', linestyle='--')
max_period = 50
repeat = 5
max_itr = 5
for i in [5]:
    for j in [3]:
        regret = np.zeros((max_itr+1, max_period))
        regret1 = np.zeros((max_itr+1, max_period))
        for k in range(1, repeat+1):
            with open('data/{0}_{1}_{2}'.format(i, j, k), 'rb') as filehandle:
                acc_regret = pickle.load(filehandle)
                acc_regret1 = pickle.load(filehandle)
                regret += acc_regret
                regret1 += acc_regret1
        regret = regret / repeat
        regret1 = regret1 / repeat
        c = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        # plt.plot(list(range(max_period)), regret, '--', color=c)
        # plt.plot(list(range(max_period)), regret1, '-', color=c)
for i in range(max_itr+1):
    plt.plot(list(range(max_period)), regret1[i, :], '--', label='{0}'.format(i))

plt.xlabel(r"$Time$", fontsize=15)
plt.ylabel(r"$R_K$", fontsize=15)


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.legend(fontsize=10)
plt.show()
