'''
(4) For a given data of heights of a class, the heights of 15 students are recorded as 
167.65, 167, 172, 175, 165, 167, 168, 167, 167.3, 170, 167.5, 170, 167, 169, and 172.  
Develop an application that computes;  
explore if there are any packages supported in your platform that depicts these measures / their calculation of central tendency in a visual form for ease of understanding.  
a. Mean height of the student 
b. Median and Mode of the sample space  
c. Standard deviation  
d. Measure of skewness.  [(Mean-Mode)/standard deviation] 
'''

def Sum(X):
    sum = 0
    for x in X:
        sum += x
    return sum

def Max(X):
    max = 0
    for x in X:
        if max < x:
            max = x
    return max

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
    BubbleSort(X)

    if len(X) % 2 == 1:
        return X[int((len(X) - 1)/2)]
    else:
        return (X[int(len(X)/2)] + X[int(len(X)/2 - 1)]) / 2

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
    SD = 0.0

    mean = Mean(X)
    sumsqaurediff = 0.0
    for x in X:
        sumsqaurediff += (x - mean) ** 2
    SD = (sumsqaurediff / len(X)) ** (1/2)

    return SD

def Skewness(X):
    return (Mean(X) - Mode(X)) / StandardDeviation(X)

def BubbleSort(arr):
    n = len(arr)

    # Traverse through all array elements
    for i in range(n):
 
        # Last i elements are already in place
        for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]

# Driver Code
data = [167.65, 167, 172, 175, 165, 167, 168, 167, 167.3, 170, 167.5, 170, 167, 169, 172]
print("Data:", data)

# a
print("Mean Height:", Mean(data))

# b
print("Median Height:", Median(data))
print("Mode Height:", Mode(data))

# c
print("Standard Deviation:", StandardDeviation(data))

# d
print("Skewness:", Skewness(data))

# Visual Representation?