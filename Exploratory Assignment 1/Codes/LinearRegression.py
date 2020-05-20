'''
Linear regression Algorithm Implementation
'''

# Imports
import numpy as np
from matplotlib import pyplot as plt

# Main Functions
def GenerateData(m, c, n_samples=450, random_scale=5, random_seed=0):
    np.random.seed(random_seed)
    x = np.arange(1, n_samples+1)
    y = c + m * x + np.random.normal(0, random_scale, n_samples)
    return x, y

def PlotData(X, Y, model=None):
    plt.plot(X, Y, "o")
    if not model == None:
        # 2 extreme points of line are (0, c) and (n, mn+c)
        x1 = 0
        y1 = model['c']
        x2 = model['n']
        y2 = model['m']*x2 + model['c']
        plt.plot([x1, x2], [y1, y2], color='k', linestyle='-', linewidth=2)
    plt.show()

def LinearRegression2D_Fit(X, Y, model=None):
    # Init
    sumX = 0
    sumX2 = 0
    sumY = 0
    sumXY = 0
    n = X.shape[0]

    # Check if retraining model
    if not model == None:
        sumX = model['sumX']
        sumX2 = model['sumX2']
        sumY = model['sumY']
        sumXY = model['sumXY']
        n += model['n']
    else:
        model = {}

    # Calculate sums
    for x, y in zip(X, Y):
        sumX += x
        sumY += y
        sumX2 += x * x
        sumXY += x * y
    
    # Calculate constants
    m = (n*sumXY - sumX*sumY) / (n*sumX2 - sumX*sumX)
    c = (sumY - m*sumX) / n

    # Update Model
    model['m'] = m
    model['c'] = c
    model['sumX'] = sumX
    model['sumX2'] = sumX2
    model['sumY'] = sumY
    model['sumXY'] = sumXY
    model['n'] = n

    return model

def LinearRegression2D_Predict(model, X):
    return model['m']*X + model['c']

# Driver Code
# Params
m = 5
c = 10
n_samples = 100
random_scale = 50
seed = 100

# Fit
# Generate Data
X, Y = GenerateData(m, c, n_samples=n_samples, random_scale=random_scale, random_seed=seed)
# Plot Data
PlotData(X, Y)
# Fit the data
model = LinearRegression2D_Fit(X, Y)
# Plot Fitted Data
PlotData(X, Y, model=model)

# Predict
X_pred = np.array([12.3, 10.1, 25.2])
Y_actual = np.multiply(X_pred, m) + c
Y_pred = LinearRegression2D_Predict(model, X_pred)

# Evaluate
print("Parameters:")
print("Slope: Actual:", m, " - Predicted:", model['m'])
print("Intercept: Actual:", c, " - Predicted:", model['c'])

print("Predictions:")
for i in range(X_pred.shape[0]):
    print("X:", X_pred[i], "Actual Y:", Y_actual[i], " - Predicted Y:", Y_pred[i])