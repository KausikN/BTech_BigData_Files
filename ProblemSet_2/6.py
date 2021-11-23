'''
6. Generate random numbers from the following distribution and visualize the data using violin plot. 
(i) Standard-Normal distribution. 
(ii) Log-Normal distribution. 
'''
import matplotlib.pyplot as plt
import numpy as np

def GenerateStandardNormalDist(n, mean=0.0, SD=1.0):
    return np.random.normal(mean, SD, (n))

def GenerateLogNormalDist(n, mean=0.0, SD=1.0):
    return np.random.lognormal(mean, SD, (n))

def ViolinPlot(X, title=''):
    plt.violinplot(X)
    plt.title(title)
    plt.show()

# Driver Code
n = 100
mean = 0.0
SD = 1.0
SNDist = GenerateStandardNormalDist(n, mean, SD)
LNDist = GenerateLogNormalDist(n, mean, SD)
ViolinPlot(SNDist, 'Standard Normal')
ViolinPlot(LNDist, 'Log Normal')
