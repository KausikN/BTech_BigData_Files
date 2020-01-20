'''
1. On New Year’s Eve, Tina walked into a random shop and surprised to see a huge crowd there. 
She is interested to find what kind of products they sell the most, for which she needs the age distribution of customers. 
Help her to find out the same using histogram. 
The age details of the customers are given below   
7, 9, 27, 28, 55, 45, 34, 65, 54, 67, 34, 23, 24, 66, 53, 45, 44, 88, 22, 33, 55, 35, 33, 37, 47, 41,31, 30, 29, 12
Identify the type of histogram (eg. Bimodal, Multimodal, Skewed..etc). Use different bin sizes.  
'''
import matplotlib.pyplot as plt
import numpy as np

def GenerateHistogram(Ages):
    n_bins = 25
    X = np.arange(len(Ages))
    n, bins, patches = plt.hist(Ages, n_bins, facecolor='blue', alpha=0.5)
    plt.show()

Ages = [7, 9, 27, 28, 55, 45, 34, 65, 54, 67, 34, 23, 24, 66, 53, 45, 44, 88, 22, 33, 55, 35, 33, 37, 47, 41,31, 30, 29, 12]
GenerateHistogram(Ages)

# FROM HISTOGRAM WE GET THAT
# DATA IS BIMODAL - 30 to 40 and 50 to 60