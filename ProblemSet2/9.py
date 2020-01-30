'''
Let's say you are the new owner of a small ice-cream shop in a little village near the beach. 
You noticed that there was more business in the warmer months than the cooler months. 
Before you alter your purchasing pattern to match this trend, you want to be sure that the relationship is real. 
Help him to find the correlation between the data given.
Temperature     Number of Customers 
98              15 
87              12 
90              10 
85              10 
95              16 
75              7
'''
import matplotlib.pyplot as plt

def Correlation(X, Y):
    n = len(X)
    sig_xy = 0
    sig_x = 0
    sig_y = 0
    sig_x2 = 0
    sig_y2 = 0
    for x, y in zip(X, Y):
        sig_xy += x*y
        sig_x += x
        sig_y += y
        sig_x2 += x**2
        sig_y2 += y**2

    corr = ((n*sig_xy) - (sig_x*sig_y)) / (((n*sig_x2 - (sig_x**2)) * (n*sig_y2 - (sig_y**2)))**(1/2))
    return corr

def Scatterplot(X, Y):
    plt.scatter(X, Y)
    plt.title('Scatter Plot')
    plt.xlabel('Temperature')
    plt.ylabel('No of Customers')
    plt.show()

# Driver Code
Temp = [98, 87, 90, 85, 95, 75]
CustNo = [15, 12, 10, 10, 16, 7]

print("Correlation:", Correlation(Temp, CustNo))
Scatterplot(Temp, CustNo)