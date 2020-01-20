'''
(9) Consider the following sample of weights for 45 individuals:  
79, 71, 89, 57, 76, 64, 82, 82, 67, 80, 81, 65, 73, 79, 79, 60, 58, 83, 74, 68, 78, 80, 78, 81, 76, 65, 70, 76, 58, 82, 59, 73, 72, 79, 87, 63, 74, 90, 69, 70, 83, 76, 61, 66, 71, 60, 57, 81, 57, 65, 81, 78, 77, 81, 81, 63, 71, 66, 56, 62, 75, 64, 74, 74, 70, 71, 56, 69, 63, 72, 81, 54, 72, 91, 92
For the above data generates histograms and depict them using packages in your platform. 
Explore the different types of histograms available and test drive the types supported in your platform.
'''
import matplotlib.pyplot as plt
import numpy as np

def GenerateHistogram(Marks):
    n_bins = 10
    X = np.arange(len(Marks))
    n, bins, patches = plt.hist(Marks, n_bins, facecolor='blue', alpha=0.5)
    plt.show()

Marks = [79, 71, 89, 57, 76, 64, 82, 82, 67, 80, 81, 65, 73, 79, 79, 60, 58, 83, 74, 68, 78, 80, 78, 81, 76, 65, 70, 76, 58, 82, 59, 73, 
        72, 79, 87, 63, 74, 90, 69, 70, 83, 76, 61, 66, 71, 60, 57, 81, 57, 65, 81, 78, 77, 81, 81, 63, 71, 66, 56, 62, 75, 64, 74, 74, 
        70, 71, 56, 69, 63, 72, 81, 54, 72, 91, 92]
GenerateHistogram(Marks)

# INCOMPLETE