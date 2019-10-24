# import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pickle
import random
import matplotlib as mp
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

# font_size = 20
# mp.rcParams['font.size'] = font_size
# mp.rcParams['axes.labelsize'] = font_size
# mp.rcParams['axes.linewidth'] = font_size / 12.
# mp.rcParams['axes.titlesize'] = font_size
# mp.rcParams['legend.fontsize'] = 14
# mp.rcParams['xtick.labelsize'] = font_size
# mp.rcParams['ytick.labelsize'] = font_size
# plt.gca().set_aspect('equal', adjustable='box')

# fig = plt.figure()
# ax = fig.add_subplot(111)
# plt.rc('font', family='serif')
# plt.rc('text', usetex=True)
# plt.grid(b=True, which='major', color='gray', linestyle='--')
# c = ['r', 'g', 'b', 'm', 'c']
# max_period = 30
# repeat = 3
# max_itr = 2
# acc_regret_init = np.zeros((max_itr+1, max_period))
# for i in [1, 2, 3, 4]:
#     for j in [10]:
#         regret = np.zeros((max_itr+1, max_period))
#         regret1 = np.zeros((max_itr+1, max_period))
#         for k in range(1, repeat+1):
#             with open('data/correct{0}_{1}_{2}'.format(i, j, k), 'rb') as filehandle:
#                 acc_regret = pickle.load(filehandle)
#                 acc_regret1 = pickle.load(filehandle)
#                 regret += acc_regret
#                 regret1 += acc_regret1
#                 acc_regret_init += acc_regret[0, :]
#                 acc_regret_init += acc_regret1[0, :]
#         regret = regret / repeat
#         regret1 = regret1 / repeat
#         # c = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
#         # plt.plot(list(range(max_period)), regret, '--', color=c)
#         # plt.plot(list(range(max_period)), regret1, '-', color=c)
#
#         plt.plot(list(range(max_period)), regret[2, :], '--', label='_nolegend_', color=c[i-1])
#         plt.plot(list(range(max_period)), regret1[2, :], '-', label=r'$N={0}$'.format(i), color=c[i-1])
#
#
# acc_regret_init = acc_regret_init / 24
# plt.plot(list(range(max_period)), acc_regret_init[0, :], '-', label=r'$m(\mathrm{x}_0)$', color='k')
# plt.xlabel(r"$\mathrm{Time}$", fontsize=16, usetex=True)
# plt.ylabel(r"$R_K$", fontsize=16, usetex=True)
# plt.xticks(fontsize=18, usetex=True)
# plt.yticks([0, 40, 80, 120], fontsize=18, usetex=True)
# plt.legend(fontsize=14)
#
# # plt.show()
# plt.savefig('/Users/chrislaw/Box Sync/Research/Zero_Opt2019/fig/10_local_full.pdf', format="pdf")

# r = 0.5
# max_period = 50
# repeat = 5
# max_itr = 5
# acc_init = np.zeros((1, max_period))
# acc_init_total = np.zeros((1, max_period))
# for i in [5]:
#     for j in [5]:
#         regret = np.zeros((max_itr+1, max_period))
#         regret1 = np.zeros((max_itr+1, max_period))
#         for k in range(1, repeat+1):
#             with open('data/today{0}_{1}_{2}'.format(i, j, k), 'rb') as filehandle:
#                 acc_regret = pickle.load(filehandle)
#                 acc_regret1 = pickle.load(filehandle)
#                 com = pickle.load(filehandle)
#                 for ii in range(max_period):
#                     acc_init[:, ii] = acc_init[:, ii - 1] + com[:, ii] if ii > 0 else com[:, ii]
#
#                 regret += acc_regret
#                 regret1 += acc_regret1
#                 acc_init_total += acc_init
#         regret = regret / repeat
#         regret1 = regret1 / repeat
#         acc_init_total = acc_init_total / repeat
#         # c = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
#         # plt.plot(list(range(max_period)), regret, '--', color=c)
#         # plt.plot(list(range(max_period)), regret1, '-', color=c)
#         fig = plt.figure()
#         ax = fig.add_subplot(111)
#         plt.rc('font', family='serif')
#         plt.rc('text', usetex=True)
#         plt.grid(b=True, which='major', color='gray', linestyle='--')
#         c = ['r', 'g', 'b', 'k', 'm', 'c']
#         for i in range(1, max_itr+1):
#             plt.plot(list(range(max_period)), regret[i, :], '--', label='_nolegend_', color=c[i])
#             plt.plot(list(range(max_period)), regret1[i, :], '-', label='$N={0}$'.format(i), color=c[i])
#         plt.plot(list(range(max_period)), acc_init_total[0, :], '-.', label=r'$m(\mathbf{x}_0)$', color='r')
#         plt.xlabel(r"$\mathrm{Time}$", fontsize=16, usetex=True)
#         plt.ylabel(r"$R_K$", fontsize=16, usetex=True)
#
#         plt.xticks(fontsize=18,usetex=True)
#         plt.yticks([0, 40, 80, 120, 160], fontsize=18,usetex=True)
#         plt.legend(fontsize=14)
#
#         plt.savefig('/Users/chrislaw/Box Sync/Research/Zero_Opt2019/fig/{0}.pdf'.format(j), format="pdf")
#
# plt.show()

# max_period = 50
# repeat = 5
# max_itr = 5
# for i in [5]:
#     for j in [5]:
#         regret0 = np.zeros((max_itr+1, max_period))
#         regret1 = np.zeros((max_itr + 1, max_period))
#         for k in range(1, repeat+1):
#             with open('data/today{0}_{1}_{2}'.format(i, j, k), 'rb') as filehandle:
#                 acc_regret0 = pickle.load(filehandle)
#                 acc_regret1 = pickle.load(filehandle)
#                 regret0 += acc_regret0
#                 regret1 += acc_regret1
#         regret0 = regret0 / repeat
#         regret1 = regret1 / repeat
#     for j in [10]:
#         regret10 = np.zeros((max_itr + 1, max_period))
#         regret11 = np.zeros((max_itr + 1, max_period))
#         for k in range(1, repeat + 1):
#             with open('data/{0}_{1}_{2}'.format(i, j, k), 'rb') as filehandle:
#                 acc_regret10 = pickle.load(filehandle)
#                 acc_regret11 = pickle.load(filehandle)
#                 regret10 += acc_regret10
#                 regret11 += acc_regret11
#         regret10 = regret10 / repeat
#         regret11 = regret11 / repeat
#         # c = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
#         # plt.plot(list(range(max_period)), regret, '--', color=c)
#         # plt.plot(list(range(max_period)), regret1, '-', color=c)
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     plt.rc('font', family='serif')
#     plt.rc('text', usetex=True)
#     plt.grid(b=True, which='major', color='gray', linestyle='--')
#     c = ['r', 'g', 'b', 'k', 'm', 'c']
#     for i in range(1, max_itr+1):
#         plt.plot(list(range(max_period)), regret1[i, :], '--', label='_nolegend_', color=c[i])
#         plt.plot(list(range(max_period)), regret11[i, :], '-', label=r'$N={0}, r=1$'.format(i), color=c[i])
#
#     plt.xlabel(r"$\mathrm{Time}$", fontsize=16, usetex=True)
#     plt.ylabel(r"$R_K$", fontsize=16, usetex=True)
#
#     plt.xticks(fontsize=18,usetex=True)
#     plt.yticks([0, 20, 40, 60, 80], fontsize=18,usetex=True)
#     plt.legend(fontsize=14)
#
#     plt.savefig('/Users/chrislaw/Box Sync/Research/Zero_Opt2019/fig/local.pdf', format="pdf")
# plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
plt.rc('font', family='serif')
plt.rc('text', usetex=True)
plt.grid(b=True, which='major', color='gray', linestyle='--')
c = ['r', 'g', 'b', 'm', 'c']
line = ['-', '--', '-.']
max_period = 30
repeat = 3
max_itr = 2
acc_regret_init = np.zeros((max_itr+1, max_period))
for index, j in enumerate([3, 5, 10]):
    for i in [3]:
        regret = np.zeros((max_itr+1, max_period))
        regret1 = np.zeros((max_itr+1, max_period))
        for k in range(1, repeat+1):
            with open('data/correct{0}_{1}_{2}'.format(i, j, k), 'rb') as filehandle:
                acc_regret = pickle.load(filehandle)
                acc_regret1 = pickle.load(filehandle)
                regret += acc_regret
                regret1 += acc_regret1
                acc_regret_init += acc_regret[0, :]
                acc_regret_init += acc_regret1[0, :]
        regret = regret / repeat
        regret1 = regret1 / repeat
        # c = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        # plt.plot(list(range(max_period)), regret, '--', color=c)
        # plt.plot(list(range(max_period)), regret1, '-', color=c)

        # plt.plot(list(range(max_period)), regret[2, :], '--', label='_nolegend_', color=c[i-1])
        plt.plot(list(range(max_period)), regret[2, :], line[index], label=r'$N={0}$'.format(i), color=c[i-1])


# acc_regret_init = acc_regret_init / 24
# plt.plot(list(range(max_period)), acc_regret_init[0, :], '-', label=r'$m(\mathrm{x}_0)$', color='k')
plt.xlabel(r"$\mathrm{Time}$", fontsize=16, usetex=True)
plt.ylabel(r"$R_K$", fontsize=16, usetex=True)
plt.xticks(fontsize=18, usetex=True)
plt.yticks([0, 40, 80, 120], fontsize=18, usetex=True)
plt.legend(fontsize=14)

plt.show()
# plt.savefig('/Users/chrislaw/Box Sync/Research/Zero_Opt2019/fig/r_full.pdf', format="pdf")