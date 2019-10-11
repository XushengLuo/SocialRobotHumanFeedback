 # code for basis

     basis = np.zeros((nx * 2, 5))
     basis[:, 0] = np.array([6., 6.8, 7., 7.4, 7.8, 8.2, 8.8, 9.2, 10., 11.4, 12.2, 13.4, 20., 0.,
                             1.8, 3.8, 5.8, 6.6, 8.4, 10.2, 11.4, 13., 14.6, 15.6, 17.2, 20.])
    
     basis[:, 1] = np.array([6., 7.48513957, 7.81997223, 8.41189715, 8.16728452, 8.4708108,
                             9.54454019, 10.26686085, 10.23037205, 11.8109363, 12.50000342,
                             13.90636496, 20., 0., 2.0736383, 4.67533416, 5.96686564, 6.86340497,
                             9.41861856, 10.78509445, 12.22915791, 14.02335437, 15.74004816,
                             15.89395627, 17.42943277, 20.])
    
     basis[:, 2] = np.array([6., 7.38689286, 7.72294127, 8.32688833, 7.95670251, 8.2823111,
                             9.52535605, 10.02413205, 10.1637055, 11.67041769, 12.35053234, 13.8070384, 20.,
                             0., 1.82531358, 4.51620829, 5.90799749, 6.79589611, 9.34822995,
                             10.73910471, 11.9835629, 13.93064889, 15.66466243, 15.67794821, 17.28655007, 20.])
    
     basis[:, 3] = np.array([6., 5.7827818, 7.14493751, 8.71040373, 6.53284159, 8.47767034, 7.65621351,
                             9.13904636, 13.82271469, 11.30440854, 13.97073257, 12.89681254, 20.,
                             0., -1.30811039, 3.2724712, 7.85075504, 8.92565511,
                             10.22626494, 9.76080429, 12.88540459, 12.96289298, 18.23389962, 17.60080336,
                             16.14748156, 20.])
     basis[:, 4] = np.array([6., 5.74133844, 7.33800593, 8.98332517, 6.50921693, 8.55970013,
                             7.61256167, 9.31338245, 13.91569761, 11.38711136, 14.09736454, 12.88094703,
                             20., 0., -1.21644538, 2.99286283, 7.82685527, 8.886719,
                             10.30002114, 9.83331944, 12.8647886, 13.0071202, 18.33810794, 17.65912744,
                             16.14631291, 20.])
     eta = 1e-1   Note: step size rule 1 does not work well when dimension is larger than 2  1e-2
     delta = 1e-1   exploration parameter
     nw = 5
     wt = np.zeros((nw, maxItr))
     wt[:, 0] = np.array([1, 0, 0, 0, 0])
     meas = np.zeros((maxItr,))   Distance me
    
     for i in range(maxItr - 1):
         x = np.reshape(np.matmul(basis, wt[:, i]), (nx*2, 1))
         s, index = human_feedback(x, human_cluster)
         meas[i] = s
         if s < 1e-2:
             break
         ut = np.random.random((nw, ))
         ut = ut / np.linalg.norm(ut)
         w_plus = wt[:, i] + ut * delta
         x_plus = np.reshape(np.matmul(basis, w_plus), (nx * 2, 1))
         s_plus, _ = human_feedback(x_plus, human_cluster)
         w_minus = wt[:, i] - ut * delta
         x_minus = np.reshape(np.matmul(basis, w_minus), (nx * 2, 1))
         s_minus, _ = human_feedback(x_minus, human_cluster)
    
         gt = nw / 2 / delta * (s_plus - s_minus) * ut   gradient
    
         wt[:, i + 1] = wt[:, i] - eta * gt.ravel()   gradient descent
         print(i, s, wt[:, i + 1])
    
     x = np.reshape(np.matmul(basis, wt[:, i]), (nx*2, 1))
     workspace_plot(x, nx, human_cluster, obstacle)
     plt.show()
 
 
 # count the number of points in the polygon
    # for polygon in human_cluster.values():
    #     cluster = Polygon(polygon)
    #     point = []
    #     for i in range(nx):
    #         if Point((x[i], x[i+nx])).within(cluster):
    #             point.append((x[i], x[i+nx]))
    #     # point in polygon
    #     if point:
    #         score += get_score(point, polygon)
    
  # workspace
  
    # w = Workspace()
    # with open('data/workspace', 'wb') as filehandle:
    #     pickle.dump(w, filehandle)
    # with open('data/case1', 'rb') as filehandle:
    #     w = pickle.load(filehandle)
    # print(w.regions)
    # w.init_goal = {'s': (6, 0), 't': (13, 17)}
    # w.plot_workspace()
    # plt.grid(b=True, which='major', color='k', linestyle='--')
    # plt.show()

# distance between the center of cluster and trajectory
    # def get_score(point, polygon):
    #     rho = 10
    #     cx, cy, r = make_circle(polygon)
    #     score = 0
    #     for p in point:
    #         score += rho/(np.linalg.norm(np.array(p) - np.array([cx, cy])))
    #     return score

# parameter
1. for distance to the center, 

eta = 1e-2  # Note: step size rule 1 does not work well when dimension is larger than 2  
delta = 1e0  # exploration parameter

2. for counting the number

eta = 1e-1  # Note: step size rule 1 does not work well when dimension is larger than 2 
delta = 1e1  # exploration parameter

3.   dist = np.sum([np.linalg.norm([x[i] - x[i + 1], x[i + nx] - x[i + 1 + nx]]) for i in range(nx - 1)])
     
     for obstacles, score += 10 or 1
     
     if np.fabs(dist-dist0) < 1 and s-dist < 1e-2:
        break
      
# result

locally perturbation works better than full perturbation when the length doubles


