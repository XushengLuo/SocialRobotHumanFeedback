import numpy as np
import matplotlib.pyplot as plt
import pickle
import random
import matplotlib


matplotlib.rcParams.update({'font.size': 16})
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
# plt.gca().set_aspect('equal', adjustable='box')
plt.grid(b=True, which='major', color='k', linestyle='--')
max_period = 100
repeat = 10
c = ['r', 'g', 'b']

# # N maximum number of iteraitons and r the movement radius
for index, i in enumerate([10, 20, 30]):
    for j in [3, 10]:
        regret = np.zeros((1, max_period)).ravel()
        regret1 = np.zeros((1, max_period)).ravel()
        for k in range(1, repeat+1):
            with open('data/{0}_{1}_{2}'.format(i, j, k), 'rb') as filehandle:
                acc_regret = pickle.load(filehandle)
                acc_regret1 = pickle.load(filehandle)
                regret += acc_regret
                regret1 += acc_regret1
        regret = regret / repeat
        regret1 = regret1 / repeat
        if j == 3:
            plt.plot(list(range(max_period)), regret, '--', color=c[index], label=r'$N={0}, r=0.{1}$'.format(i, j))
        else:
            plt.plot(list(range(max_period)), regret, '-', color=c[index], label=r'$N={0}, r={1}$'.format(i, j//10))
plt.legend(loc=2, prop={'size': 12})
plt.xlabel('Time', fontsize=12)
plt.ylabel('$R_T$', fontsize=12)
plt.show()

# N maximum number of iteraitons and full/local
# for index, i in enumerate([10, 20, 30]):
#     for j in [10]:
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
#         plt.plot(list(range(max_period)), regret, '--', color=c[index], label=r'$N={0}, full$'.format(i))
#         plt.plot(list(range(max_period)), regret1, '-', color=c[index], label=r'$N={0}, local$'.format(i))
# plt.legend(loc=2, prop={'size': 12})
# plt.xlabel('Time', fontsize=12)
# plt.ylabel('$R_T$', fontsize=12)
# plt.show()