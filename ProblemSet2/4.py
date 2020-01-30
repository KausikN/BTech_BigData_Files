'''
4. A car company wants to predict how much fuel different cars will use based on their masses. 
They took a sample of cars, drove each car 100km, and measured how much fuel was used in each case (in litres). 
Visualize the data using scatterplot and also find co-relation between the 2 variables 
(eg. Positive//Negative, Linear/ Non-linear co-relation) The data is summarized in the table below.  
(Use a reasonable scale on both axes and put the explanatory variable on the x-axis.) 
Fuel used 
(L)                     3.6 6.7 9.8 11.2 14.7 
Mass (metric tons)      0.45 0.91 1.36 1.81 2.27 
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
    plt.xlabel('Mass')
    plt.ylabel('Litres')
    plt.show()

# Driver Code
Mass = [0.45, 0.91, 1.36, 1.81, 2.27]
L = [3.6, 6.7, 9.8, 11.2, 14.7]

print(Correlation(Mass, L))

Scatterplot(Mass, L)

# Positive Correlation