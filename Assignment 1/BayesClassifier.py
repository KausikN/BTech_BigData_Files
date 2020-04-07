'''
Bayes Classification Test Drive
'''
# Imports
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

def ImportDataset_Iris():
    iris = load_iris()
    return iris

def SplitDataset(Dataset):
    # Separate Target Field from Dataset
    X = Dataset.data
    Y = Dataset.target

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=1)

    return X, Y, X_train, X_test, Y_train, Y_test

def Train(X_train, Y_train):
    BayesClassifier = GaussianNB()
    BayesClassifier.fit(X_train, Y_train)
    return BayesClassifier

def Predict(GaussianClassifier, X_test):
    Y_pred = GaussianClassifier.predict(X_test)
    print("Predicted values:")
    print(Y_pred)
    return Y_pred

def PrintAccuracy(Y_test, Y_pred):
    print("Confusion Matrix:\n", confusion_matrix(Y_test, Y_pred))
    print("Accuracy:\n", accuracy_score(Y_test, Y_pred)*100)
    print("Report:\n", classification_report(Y_test, Y_pred))

# Driver Code

print("\n\n")

# Building Phase
Dataset = ImportDataset_Iris()
X, Y, X_train, X_test, Y_train, Y_test = SplitDataset(Dataset)
BayesClassifier = Train(X_train, Y_train)

print("\n\n")

# Operational Phase
# Prediction using Gini
print("Results Using Bayes Classifier:")
Y_pred = Predict(BayesClassifier, X_test)
PrintAccuracy(Y_test, Y_pred)

print("\n\n")