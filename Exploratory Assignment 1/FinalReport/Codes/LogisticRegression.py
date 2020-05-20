'''
Logistic regression Algorithm Implementation
'''

# Imports
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Main Functions
def LoadIrisData():
    iris = datasets.load_iris()
    x = np.array(iris.data[0:99, :2])
    y = np.array(iris.target[0:99])
    return x, y

def PlotData(X, labels=[], title='Plot'):
    if len(labels) == 0:
        plt.scatter(X[:, 0], X[:, 1], alpha=0.7, edgecolors='b')
    else:
        plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='rainbow', alpha=0.7, edgecolors='b')
    plt.title(title)
    plt.show()

def Sigmoid_Predict(Data, w, b):
    Z = np.dot(w.T, Data.T) + b
    return 1 / (1 + 1/np.exp(Z))

def GradientDescent(Data, Target, lr=0.01, epochs=1000, w=None, b=None, recordInterval=1):
    #Step 1: Initial Model Parameter
    N = len(Data)
    if w == None:
        w = np.zeros((2,1))
    if b == None:
        b = 0
    costs = []
    for i in tqdm(range(epochs)):
        #Step 2: Apply sigmoid Function and get y prediction
        y_pred = Sigmoid_Predict(Data, w, b)
        #Step 3: Calculate Cost Function
        cost = -(1/N) * np.sum(Target * np.log(y_pred) + (1-Target) * np.log(1-y_pred))
        #Step 4: Calculate Gradient
        dw = 1/N * np.dot(Data.T, (y_pred-Target).T)
        db = 1/N * np.sum(y_pred-Target)
        #Step 5: Update w & b
        w = w - lr * dw
        b = b - lr * db
        #Records cost
        if i % recordInterval == 0:
            costs.append(cost)
    return costs, w, b

def PlotLoss(losses):
    losses = np.array(losses)
    plt.plot(np.arange(1, losses.shape[0]+1), losses)
    plt.title('Loss vs Epoch')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.show()

# Driver Code
# Load Data
Data, Target = LoadIrisData()
# Plot Data
PlotData(Data, labels=Target, title='Original')

# Do Gradient Descent and fit the data
# Params
lr=0.01
epochs=1000000
w=None
b=None
recordInterval=1000

losses, w_final, b_final = GradientDescent(Data, Target, lr=lr, epochs=epochs, w=w, b=b, recordInterval=recordInterval)
# Plot Loss
PlotLoss(losses)

# Predict
Y_Pred = Sigmoid_Predict(Data, w_final, b_final)
Y_Pred = np.reshape(Y_Pred, Y_Pred.shape[1])
print(Y_Pred)
Y_Pred_final = []
for yp in Y_Pred:
    if yp >= 0.5:
        Y_Pred_final.append(1)
    else:
        Y_Pred_final.append(0)

PlotData(Data, labels=Y_Pred_final, title='Predicted')