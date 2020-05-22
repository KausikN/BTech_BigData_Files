'''
Test driving K-Means Clustering Algorithm
'''
# Imports
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

# Main Functions
# def AgglomerativeClustering(items):
#     cluster_points = []
#     cluster_names = []

#     # Initially all points are clusters
#     index = 0
#     for item in items:
#         cluster_points.append(item)
#         cluster_names.append([index])
#         index += 1
    
#     # Find proximity matrix
#     Prox_Matrix = ProximityMatrix(cluster_points)

#     # Merge Nearest Clusters
#     cluster_names_new = cluster_names.copy()
#     cluster_points_new = cluster_points.copy()
#     merged_indices = []
#     merged_values = []
#     for i in range(len(cluster_points)):
#         if i in merged_indices:
#             continue
#         closest_index = -1
#         closest_value = -1
#         for j in range(i+1, len(cluster_points)):
#             if j in merged_indices:
#                 continue
#             if closest_value == -1 or Prox_Matrix[str(i) + "_" + str(j)] < closest_value:
#                 closest_index = j
#                 closest_value = Prox_Matrix[str(i) + "_" + str(j)]
#         if closest_index > -1:

#             merged_indices.append(closest_index)



# Driver Code
# items = np.array([
#         [5,3],
#         [10,15],
#         [15,12],
#         [24,10],
#         [30,30],
#         [85,70],
#         [71,80],
#         [60,78],
#         [70,55],
#         [80,91]
#                 ])

minval = 0
maxval = 100
n_points = 100
N_Clusters = 3

# Generate Random Points
items = np.random.randint(minval, maxval+1, (n_points, 2))

plt.scatter(items[:,0], items[:,1])
plt.show()

# Clustering
Cluster = KMeans(n_clusters=N_Clusters)
Cluster.fit_predict(items)

plt.scatter(items[:,0], items[:,1], c=Cluster.labels_, cmap='rainbow')
plt.show()