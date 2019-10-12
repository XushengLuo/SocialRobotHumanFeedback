import numpy as np
from numpy import linspace
import matplotlib.pyplot as plt


X, Y = np.meshgrid(linspace(0, 1), linspace(0, 1))
q = plt.quiver(X, Y, np.random.random((1, 1)), np.random.random((1, 1)))
plt.draw()
plt.pause(2)
q.set_offsets(q.get_offsets() * np.array([1, .5]))
plt.draw()
plt.show()