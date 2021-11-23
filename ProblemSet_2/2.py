'''
2. A Coach tracked the number of points that each of his 30 players on the team had in one game. 
The points scored by each player is given below. 
Visualize the data using ordered stem-leaf plot and also detect the outliers and shape of the distribution. 
22, 21, 24, 19, 27, 28, 24, 25, 29, 28, 26, 31, 28, 27, 22, 39, 20, 10, 26, 24, 27, 28, 26, 28, 18, 32, 29, 25, 31, 27
'''
import matplotlib.pyplot as plt
import numpy as np

def Generate_Stems_Leaves(data, leaflen):
    leaves = []
    stems = []
    for d in data:
        leaves.append(int(str(d)[(-1*leaflen):]))
        stems.append(int(str(d)[:(-1*leaflen)]))
    return stems, leaves

def GenerateStemPlot(stems, leaves):
    plt.title('Stem and Leaf Plot')
    plt.xlabel('Stems')
    plt.ylabel('Leaves')
    markerline, stemlines, baseline = plt.stem(stems, leaves)
    plt.show()

# Driver Code
data = [22, 21, 24, 19, 27, 28, 24, 25, 29, 28, 26, 31, 28, 27, 22, 39, 20, 10, 26, 24, 27, 28, 26, 28, 18, 32, 29, 25, 31, 27]
stems, leaves = Generate_Stems_Leaves(data, 1)
GenerateStemPlot(stems, leaves)