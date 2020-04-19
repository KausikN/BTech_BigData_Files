import numpy as np

items = [(3, 4), (7, 5), (2, 6), (3, 1),
        (8, 2), (7, 3), (4, 4), (6, 6),
        (7, 4), (6, 7)]


def AgglomerativeClustering(items):
    cluster_points = []
    cluster_names = []

    # Initially all points are clusters
    index = 0
    for item in items:
        cluster_points.append(item)
        cluster_names.append([index])
        index += 1
    
    # Find proximity matrix
    Prox_Matrix = ProximityMatrix(cluster_points)

    # Merge Nearest Clusters
    cluster_names_new = cluster_names.copy()
    cluster_points_new = cluster_points.copy()
    merged_indices = []
    merged_values = []
    for i in range(len(cluster_points)):
        closest_index = i+1
        closest_value = -1
        for j in range(i+1, len(cluster_points)):
            if closest_value == -1 or Prox_Matrix[str(i) + "_" + str(j)] < closest_value:
                closest_index = j
                closest_value = Prox_Matrix[str(i) + "_" + str(j)]
        if not closest_index in merged_indices:


                
