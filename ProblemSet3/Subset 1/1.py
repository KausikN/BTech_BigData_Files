'''
1. Suppose that the data for analysis includes the attribute age. 
The age values for the data tuples are (in increasing order) 
13, 15, 16, 16, 19, 20, 20, 21, 22, 22, 25, 25, 25, 25, 30, 33, 33, 35, 35, 35, 35, 36, 40, 45, 46, 52, 70
(a) Use min-max normalization to transform the value 25 for age onto the range [0:0;1:0]. 
(b) Use z-score normalization to transform the value 25 for age, where the standard deviation of age is 12.94 years. 
(c) Use normalization by decimal scaling to transform the value 25 for age such that transformed value is < 1 
'''
import numpy as np

def MinMaxNorm(X):
    minVal = min(X)
    maxVal = max(X)
    X_Norm = []
    for x in X:
        X_Norm.append(round((x - minVal) / (maxVal - minVal), 2))
    return X_Norm

def ZScoreNorm(X, mean, SD):
    X_Norm = []
    for x in X:
        X_Norm.append(round(((x - mean) / SD), 2))
    return X_Norm

def DecimalScaleNorm(X):
    maxVal = max(X)
    divpow = len(str(maxVal))
    X_Norm = []
    for x in X:
        X_Norm.append(round((x / (10 ** divpow)), 2))
    return X_Norm

# Driver Code
Data = [13, 15, 16, 16, 19, 20, 20, 21, 22, 22, 25, 25, 25, 25, 30, 33, 33, 35, 35, 35, 35, 36, 40, 45, 46, 52, 70]
MinMaxNormData = MinMaxNorm(Data)
ZScoreNormData = ZScoreNorm(Data, 25.0, 12.94)
DecimalScaleNormData = DecimalScaleNorm(Data)

print("Data:", Data, "\n")
print("MinMax:", MinMaxNormData, "\n")
print("ZScore:", ZScoreNormData, "\n")
print("DecimalScale:", DecimalScaleNormData)

