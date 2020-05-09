'''
BIRCH
Balanced Iterative Reducing and Clustering using Hierarchies Algorithm Implementation
'''

# Imports
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import Birch

import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()

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

def BIRCH_Library_Train(X, branching_factor=50, n_clusters=None, threshold=1.5):
    # Train Model on Input Data
    brc = Birch(branching_factor=branching_factor, n_clusters=n_clusters, threshold=threshold)
    brc.fit(X)
    return brc

def BIRCH_Library(model, X):
    labels = model.predict(X)
    return labels

# Driver Code
n_samples=450
centers=6
cluster_std=0.7
random_state=0

branching_factor = 50
n_clusters = None
threshold = 1.5

# Generate Data
X, clusters = GenerateData(n_samples=n_samples, centers=centers, cluster_std=cluster_std, random_state=random_state)
PlotData(X)

# Train and Test Model
brc = BIRCH_Library_Train(X, branching_factor=branching_factor, n_clusters=n_clusters, threshold=threshold)
labels = BIRCH_Library(brc, X)

# Plot Results
PlotData(X, labels=labels)