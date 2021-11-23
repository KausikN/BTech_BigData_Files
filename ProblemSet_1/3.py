'''
(3) For a sample space of 20 elements,
the values are fitted to the line Y=2X+3, X>5. 
Develop an application that sets up the data and computes the standard deviation of this sample space. 
(use random number generator supported in your development platform to generate values of X)
'''
import random

def GenerateData(n_data, MaxVal):
    X = []
    Y = []
    for i in range(n_data):
        x = random.randint(6, MaxVal)
        y = (2 * x) + 3
        X.append(x)
        Y.append(y)
    return X, Y

def Mean(X):
    sum = 0
    for x in X:
        sum += x
    return sum / len(X)

def StandardDeviation(X):
    SD = 0.0

    mean = Mean(X)
    sumsqaurediff = 0.0
    for x in X:
        sumsqaurediff += (x - mean) ** 2
    SD = (sumsqaurediff / len(X)) ** (1/2)

    return SD

# Driver Code
n_data = int(input("Enter no of data points: "))
MaxVal = 100
X, Y = GenerateData(n_data, MaxVal)
print("Points: ")
i = 0
for x, y in zip(X, Y):
    print(str(i+1) + ": (", x, ",", y, ")")
    i += 1
print("Standard Deviation of X:", StandardDeviation(X))
print("Standard Deviation of Y:", StandardDeviation(Y))