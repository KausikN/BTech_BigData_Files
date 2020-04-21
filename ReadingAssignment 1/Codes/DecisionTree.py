'''
Decision Tree Classifier Test Drive
'''
# Imports
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# Functions
def ImportDataset(dataset_path):
    # Import Dataset
    balance_data = pd.read_csv(dataset_path, sep= ',')#, header = None)

    # Print Dataset Size
    print ("Dataset Length: ", len(balance_data))
    print ("Dataset Shape: ", balance_data.shape)
      
    # Print Dataset Obseravtions
    print ("Dataset: ",balance_data.head())
    return balance_data

def SplitDataset(balance_data):
    # Separate Target Field from Dataset
    X = balance_data.values[:, 1:]
    Y = balance_data.values[:, 0]

    # Split Dataset into train and test
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state = 100)
      
    return X, Y, X_train, X_test, Y_train, Y_test

def Train_Gini(X_train, Y_train):
    # Create Decision Tree
    DT_Gini = DecisionTreeClassifier(
        criterion="gini", random_state=100,
        max_depth=3, min_samples_leaf=5)

    # Train
    DT_Gini.fit(X_train, Y_train)
    return DT_Gini

def Train_Entropy(X_train, Y_train):
    # Create Decision Tree
    DT_Entropy = DecisionTreeClassifier(
        criterion = "entropy", random_state = 100,
        max_depth = 3, min_samples_leaf = 5)

    # Train
    DT_Entropy.fit(X_train, Y_train)
    return DT_Entropy

def Predict(X_test, clf_object):
    # Predicton on test with Gini Index
    Y_pred = clf_object.predict(X_test)
    print("Predicted values:")
    print(Y_pred)
    return Y_pred

def PrintAccuracy(Y_test, Y_pred):
    print("Confusion Matrix:\n", confusion_matrix(Y_test, Y_pred))
    print("Accuracy:\n", accuracy_score(Y_test, Y_pred)*100)
    print("Report:\n", classification_report(Y_test, Y_pred))


# Driver code
Dataset_Path = 'Assignment 1/balance-scale.csv'

print("\n\n")

# Building Phase
Dataset = ImportDataset(Dataset_Path)
X, Y, X_train, X_test, Y_train, Y_test = SplitDataset(Dataset)
DT_Gini = Train_Gini(X_train, Y_train)
DT_Entropy = Train_Entropy(X_train, Y_train)

print("\n\n")
    
# Operational Phase
# Prediction using Gini
print("Results Using Gini Index:")
Y_pred_Gini = Predict(X_test, DT_Gini)
PrintAccuracy(Y_test, Y_pred_Gini)

print("\n\n")

# Prediction using Entropy
print("Results Using Entropy:")
Y_pred_Entropy = Predict(X_test, DT_Entropy)
PrintAccuracy(Y_test, Y_pred_Entropy)

print("\n\n")
