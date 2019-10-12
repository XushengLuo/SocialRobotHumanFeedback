import matplotlib
import numpy,matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
fig = plt.figure()
axe = fig.add_subplot(111)
polyval = numpy.random.rand(4,2) # Create the sequence of 4 2D points
patches = [Polygon(polyval,True)]
p = PatchCollection(patches,cmap=matplotlib.cm.jet,alpha=0.3)
p.set_array(100.*numpy.random.rand(1)) # Set a random color on jet map
axe.add_collection(p)
fig.colorbar(p)
fig.show()
for patch in patches:
   axe.add_patch(Polygon(patch.get_xy(),closed=True,ec='k',lw=3,fill=False)) #draw the contours
fig.canvas.draw()
plt.show()