'''
3. For a sample space of 15 people, a statistician wanted to know the consumption of water and other beverages. 
He collected their average consumption of water and beverages for 30 days (in litres). 
Help him to visualize the data using density plot, rug plot and identify the mean, median, mode and skewness of the data from the plot.
WATER       3.2, 3.5, 3.6, 2.5, 2.8, 5.9, 2.9, 3.9, 4.9, 6.9, 7.9, 8.0, 3.3, 6.6, 4.4  
BEVERAGES   2.2, 2.5, 2.6, 1.5, 3.8, 1.9, 0.9, 3.9, 4.9, 6.9, 0.1, 8.0, 0.3, 2.6, 1.4  
'''
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def Sum(X):
    return np.sum(np.array(X))

def Max(X):
    return np.max(np.array(X))

def FreqDist(X):
    freq = {}
    for x in X:
        freq[x] = 0
    for x in X:
        freq[x] += 1
    return freq

def Mean(X):
    return Sum(X) / len(X)

def Median(X):
    return np.median(np.array(X))

def Mode(X):
    modex = -1
    modex_freq = -1

    freq = FreqDist(X)

    for key in freq.keys():
        if freq[key] > modex_freq:
            modex = key
            modex_freq = freq[key]

    return modex

def StandardDeviation(X):
    return np.std(np.array(X))

def Skewness(X):
    return (Mean(X) - Mode(X)) / StandardDeviation(X)

def DensityPlot(X, labels):
    for x, label in zip(X, labels):
        sns.distplot(x, hist = False, kde = True,
                    kde_kws = {'linewidth': 3},
                    label = label)
    
    # Plot formatting
    plt.legend(prop={'size': 16}, title = 'Water vs Beverage')
    plt.title('Density Plot')
    plt.xlabel('Days')
    plt.ylabel('Consumption')
    plt.show()

def RugPlot(X, labels):
    for x, label in zip(X, labels):
        sns.rugplot(x, label=label)
    plt.title('Rug Plot')
    plt.xlabel('Days')
    plt.ylabel('Consumption')
    plt.show()

# Driver Code
WATER = [3.2, 3.5, 3.6, 2.5, 2.8, 5.9, 2.9, 3.9, 4.9, 6.9, 7.9, 8.0, 3.3, 6.6, 4.4]
BEVERAGES = [2.2, 2.5, 2.6, 1.5, 3.8, 1.9, 0.9, 3.9, 4.9, 6.9, 0.1, 8.0, 0.3, 2.6, 1.4]

print("WATER analysis:")
print("Mean:", Mean(WATER))
print("Median:", Median(WATER))
print("Mode:", Mode(WATER))
print("Skewness:", Skewness(WATER))

print("BEVERAGES analysis:")
print("Mean:", Mean(BEVERAGES))
print("Median:", Median(BEVERAGES))
print("Mode:", Mode(BEVERAGES))
print("Skewness:", Skewness(BEVERAGES))

RugPlot([WATER, BEVERAGES], ['Water', 'Beverages'])

# RUG PLOT AND DENSITY PLOT LEFT