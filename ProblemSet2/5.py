'''
5. The data below represents the number of chairs in each class of a government high school. 
Create a box plot and swarm plot (add jitter) and find the number of data points that are outliers.  
35, 54, 60, 65, 66, 67, 69, 70, 72, 73, 75, 76, 54, 25, 15, 60, 65, 66, 67, 69, 70, 72, 130, 73, 75, 76 
'''
import matplotlib.pyplot as plt
import seaborn as sns

def BoxPlot(X):
    plt.boxplot(X)
    plt.title('Box Plot')
    plt.xlabel('')
    plt.ylabel('No of Chairs')
    plt.show()

def SwarmPlot(X):
    sns.swarmplot(X)
    plt.title('Swarm Plot')
    plt.xlabel('No of Chairs')
    plt.ylabel('')
    plt.show()

def JitteredBoxPlot(X):
    sns.boxplot(data=X)
    sns.swarmplot(data=X, color='grey')
    plt.title('Box Plot')
    plt.xlabel('')
    plt.ylabel('No of Chairs')
    plt.show()

# Driver Code
Chairs = [35, 54, 60, 65, 66, 67, 69, 70, 72, 73, 75, 76, 54, 25, 15, 60, 65, 66, 67, 69, 70, 72, 130, 73, 75, 76]
# BoxPlot(Chairs)
# SwarmPlot(Chairs)
JitteredBoxPlot(Chairs)