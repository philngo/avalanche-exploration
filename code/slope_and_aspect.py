import numpy as np

dem_data_S = np.array([[1,0,-1],[1,0,-1],[1,0,-1]],dtype=np.float)
dem_data_W = np.array([[1,1,1],[0,0,0],[-1,-1,-1]],dtype=np.float)
dem_data_N = np.array([[-1,0,1],[-1,0,1],[-1,0,1]],dtype=np.float)
dem_data_E = np.array([[-1,-1,-1],[0,0,0],[1,1,1]],dtype=np.float)

gradient_S = np.gradient(dem_data_S)
gradient_W = np.gradient(dem_data_W)
gradient_N = np.gradient(dem_data_N)
gradient_E = np.gradient(dem_data_E)


