'''
Agglomerative Clustering Implementation
'''

# Imports
import numpy as np
import matplotlib.pyplot as plt

# Main Functions
def ClosestPoints(Points):
    min_distance = None
    min_points = (-1, -1)
    for i in range(len(Points)):
        for j in range(i+1, len(Points)):
            dist = Dist(Points[i], Points[j])
            if min_distance == None or min_distance > dist:
                min_distance = dist
                min_points = (i, j)
    return min_distance, min_points

def MeanPoint(A, B):
    C = []
    for a, b in zip(A, B):
        C.append((a+b)/2)
    return C

def Dist(A, B):
    return (((A[0] - B[0])**2) + ((A[1] - B[1])**2)) ** (0.5)

def AgglomerativeClustering(items, n_clusters):
    Clusters = []
    ClusterPoints = []

    # Initially every item is a cluster
    for pi in range(len(items)):
        Clusters.append([pi])
        ClusterPoints.append(items[pi])

    new_Clusters = Clusters
    new_ClusterPoints = ClusterPoints
    iteration = 1
    while(len(new_Clusters) > n_clusters):
        Clusters = new_Clusters
        ClusterPoints = new_ClusterPoints

        # Find Closest Points
        min_dist, closest_points = ClosestPoints(ClusterPoints)

        # Merge the closest points
        # Remove to be merged
        new_ClusterPoints = RemoveIndices(new_ClusterPoints, closest_points)
        new_Clusters = RemoveIndices(new_Clusters, closest_points)

        # Add merged
        this_cluster = list(np.append(np.array(Clusters[closest_points[0]]), np.array(Clusters[closest_points[1]])))
        mean_point = MeanPoint(ClusterPoints[closest_points[0]], ClusterPoints[closest_points[1]])
        new_Clusters.append(this_cluster)
        new_ClusterPoints.append(mean_point)
        print(iteration)
        print("len:", len(new_Clusters))
        print(Clusters[closest_points[0]])
        print(Clusters[closest_points[1]])
        print(this_cluster)
        print(mean_point)

        iteration += 1
    Clusters = new_Clusters
    ClusterPoints = new_ClusterPoints

    ClusterMap = {}
    for cluster_index in range(len(Clusters)):
        for p in Clusters[cluster_index]:
            ClusterMap[str(p)] = cluster_index

    return ClusterMap, ClusterPoints

def Plot(Points, corres_cluster):
    Points = np.array(Points)
    if corres_cluster == None:
        plt.scatter(Points[:, 0], Points[:, 1])
    else:
        plt.scatter(Points[:, 0], Points[:, 1], c=corres_cluster, cmap='rainbow')
    plt.show()

def RemoveIndices(Items, Indices):
    new_Items = []
    for i in range(len(Items)):
        if not i in Indices:
            new_Items.append(Items[i])
    return new_Items


# Driver Code
Points = [(3, 4), (7, 5), (2, 6), (3, 1),
        (8, 2), (7, 3), (4, 4), (6, 6),
        (7, 4), (6, 7)]

n_clusters = 3

Plot(Points, None)

min_distance, min_points = ClosestPoints(Points)

print("Min Distance:", min_distance)
print("Closest Points:", Points[min_points[0]], Points[min_points[1]])

ClusterMap, ClusterPoints = AgglomerativeClustering(Points, n_clusters)

corres_cluster = []
for pi in range(len(Points)):
    corres_cluster.append(ClusterMap[str(pi)])
Plot(Points, corres_cluster)
