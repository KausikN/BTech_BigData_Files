from sklearn.cluster import AgglomerativeClustering 
import numpy as np 
  
# randomly chosen dataset 
X = np.array([[1, 2], [1, 4], [1, 0], 
              [4, 2], [4, 4], [4, 0]]) 
  
# here we need to mention the number of clusters  
# otherwise the result will be a single cluster 
# containing all the data 
clustering = AgglomerativeClustering(n_clusters = 2).fit(X) 
  
# print the class labels 
print(clustering.labels_) 