'''
DBSCAN
Density-based Spatial Clustering of Applications with Noise Algorithm Implementation
'''

# Imports
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn import datasets
import matplotlib.pyplot as plt

# Main Functions
def GenerateData(n_samples=450, centers=6, cluster_std=0.7, random_state=0):
    X, clusters = make_blobs(n_samples=n_samples, centers=centers, cluster_std=cluster_std, random_state=random_state)
    return X, clusters

def PlotData(X, labels=[]):
    if len(labels) == 0:
        plt.scatter(X[:,0], X[:,1], alpha=0.7, edgecolors='b')
    else:
        plt.scatter(X[:,0], X[:,1], c=labels, cmap='rainbow', alpha=0.7, edgecolors='b')
    plt.show()

# def DBSCAN(dataset, eps, MinPts):
#     # cluster index
#     C = 1
#     for each unvisited point p in dataset:
#             mark p as visited
#             # find neighbors
#             Neighbors N = find the neighboring points of p

#             if |N|>=MinPts:
#                 N = N U N'
#                 if p' is not a member of any cluster:
#                     add p' to cluster C

def DBSCAN_Library(X, eps=0.3, min_samples=10, plot=True):
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    if plot:
        # Plot
        # Black removed and is used for noise instead.
        unique_labels = set(labels)
        colors = ['y', 'b', 'g', 'r']
        print("Using Colors:", colors)
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = 'k'

            class_member_mask = (labels == k)

            xy = X[class_member_mask & core_samples_mask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                                            markeredgecolor='k', 
                                            markersize=6)

            xy = X[class_member_mask & ~core_samples_mask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                                            markeredgecolor='k',
                                            markersize=6)

        plt.title('number of clusters: ' + str(n_clusters))
        plt.show()

    return labels

# Driver Code
n_samples=450
centers=3
cluster_std=0.7
random_state=0

eps=0.3
min_samples=10
plot=True

# Generate Data
X, clusters = GenerateData(n_samples=n_samples, centers=centers, cluster_std=cluster_std, random_state=random_state)
PlotData(X)

# Apply Algorithm and Plot
labels = DBSCAN_Library(X, eps=eps, min_samples=min_samples, plot=plot)
# PlotData(X, labels)