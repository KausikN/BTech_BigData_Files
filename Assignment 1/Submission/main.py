'''
Main Code to run implementations
'''

# Imports
import Preprocessing as pre
import Algorithms as algo
import DecisionTree as dt
import BayesClassifier as bc

# Driver Code
# - Preprocessing ------------------------------------------------------------------------------------------------
print("- Preprocessing ------------------------------------------------------------------------------------------------")
# Open and Clean Dataset
dataset_path = 'Dataset.csv'
Dataset = pre.ReadCSVFile(dataset_path)

# Print Dataset
print("Dataset Row Count:", len(Dataset['Symbol']))
print("Dataset: 5 rows: ")
print(Dataset.head(n=5))

print("\n\n")

# Vis Freq of Dataset
print("Dataset Freq Visualistion...")
print("Number of unique entries:")
for key in Dataset.keys():
    Freq = pre.FreqDist(Dataset[key])
    data, labels = pre.SplitDict(Freq)
    print(key, "-", len(labels))
    #print(key, ":\n", FreqDist(Dataset[key]), "\n\n")
    #BarGraph(data, labels)

print("\n\n")

# Vis Missing Dataset
print("Missing Count:")
for key in Dataset.keys():
    missing, indices = pre.MissingCount(Dataset[key])
    print(key, "-", missing)

print("\n\n")

# Clean Missing Data
print("Cleaning Dataset...")

# CLEANING PROCEDURE ----------------------

# MISSING DATA CLEAN
# This Dataset is completely text based -- so no math values
# Therefore, cleaning missing values using mean or median methods makes no sense
# Mode Replacement can be used but again it does not make exact sense as any field can have any value - not necc the most appeared value

# Only Option is to remove data if missing or leave it as it is - Depends on the field of the missing data
# Symbol                -   CANT BE NULL    -   NOT REPLACABLE
# Synonym Symbol        -   CAN BE NULL     -   REPLACABLE
# Scientific Name       -   CANT BE NULL    -   NOT REPLACABLE
# National Common Name  -   CAN BE NULL     -   REPLACABLE
# Family                -   CAN BE NULL     -   REPLACABLE

# So, if missing data in field [Symbol , Scientific Name], remove that row - As replacement makes no sense - as unique
# If missing data in REPLACABLE field, first replace by a marker value - NULL
# For field Synonym Symbol - No need to replace as it is optional field
# For National Common Name and Family - replace SMARTLY
# If there exists a subset of Scientific Name somewhere in another data row, set common name as that common name - AS COMMON NAME OF SUBSPECIES IS SAME AS COMMON NAME OF SPECIES

print("Cleaning Missing Data...")
Dataset_MissingCleaned, n_removed, n_replaced = pre.MissingClean(Dataset)
print("\n")
print("Removed", n_removed, "data rows")
print("Replaced", n_replaced, "data rows")
print("\n")
print("Cleaned Dataset Missing Count:")
for key in Dataset.keys():
    missing, indices = pre.MissingCount(Dataset[key])
    print(key, "-", missing)

print("\n\n")

# REDUNDANT DATA CLEAN
# Dataset also contains some repeated data rows
# Basic Cleaning - Search for duplicate data rows and remove all duplicates
# Advanced Cleaning - Remove row even if it is a subset of the data of any other row - REDUNDANT - IN THIS DATASET DONT DO

Dataset_RedundantCleaned, n_duplicates = pre.RedundantClean(Dataset_MissingCleaned)
print("\n")
print("Removed", n_duplicates, "duplicate data rows")
print("\n")
print("Redundant Cleaned Dataset Row Count:", len(Dataset_RedundantCleaned['Symbol']))

print("\n\n")

# Final Cleaned Dataset
Dataset_Cleaned = Dataset_RedundantCleaned

# Save Cleaned Dataset
pre.WriteCSVFile(Dataset_Cleaned, 'Dataset_Cleaned.csv')

# Encode Dataset
print("Encoding Dataset...")
Data_Transformed, LabelIndexMaps = pre.EncodeDataset(Dataset_Cleaned)
print("Encoded Dataset: 5 Rows:")
print(Data_Transformed.head(n=5))
print(LabelIndexMaps)

# Save Encoded Dataset
pre.WriteCSVFile(Data_Transformed, 'Dataset_Cleaned_Encoded.csv')
pre.pickle.dump(LabelIndexMaps, open('LabelIndexMaps.p', 'wb'))

# Visualise Preprocessed Data - Family Distribution
pre.Histogram(Data_Transformed['Family'], len(LabelIndexMaps['Family']), 'Family Name', 'Frequency', 'Family Frequency')

print("\n\n")
# - Preprocessing ------------------------------------------------------------------------------------------------

# - Part A - FIM Algos ------------------------------------------------------------------------------------------------
print("- Part A - FIM Algos ------------------------------------------------------------------------------------------------")
dataset_path = 'Dataset_Cleaned.csv'
#LabelIndexMap_path = 'LabelIndexMaps.p'

Dataset_Preprocessed = algo.ReadCSVFile(dataset_path)
#LabelIndexMap = pickle.load(open(LabelIndexMap_path, 'rb'))

# Print Dataset
DatasetRowCount = len(Dataset_Preprocessed['Symbol'])
print("Dataset Row Count:", DatasetRowCount)
print("Dataset: 5 rows: ")
print(Dataset_Preprocessed.head(n=5))

print("\n")

# Encode Dataset
### - Change to limit size of dataset encoded
DatasetPortionPercentage = 0.005
### - Change to limit size of dataset encoded
Dataset_PortionSize = int(DatasetPortionPercentage * DatasetRowCount)
if Dataset_PortionSize > DatasetRowCount:
    Dataset_PortionSize = DatasetRowCount
print("Operating on", Dataset_PortionSize, " data rows.")
print("Encoding...")
Dataset_TE = algo.OneHotEncoder(Dataset_Preprocessed.head(Dataset_PortionSize))

print("\n\n")

# FIM
# Apriori
print("Apriori")

MinimumSupport = 0.1
MinimumThreshold = 1

print("Minimum Support -", MinimumSupport)
print("Minimum Threshold -", MinimumThreshold)

FI = algo.Apriori(Dataset_TE, min_support=MinimumSupport)
RuleSet = algo.RuleMining(FI, min_threshold=MinimumThreshold)
print("Frequent Itemsets:\n", FI)
print("\n\n")
print("RuleSet:\n", RuleSet.head)
print("\n\n")

# FPGrowth
print("FPGrowth")
MinimumSupport = 0.1
MinimumThreshold = 1

print("Minimum Support -", MinimumSupport)
print("Minimum Threshold -", MinimumThreshold)

FI = algo.FPGrowth(Dataset_TE, min_support=MinimumSupport)
RuleSet = algo.RuleMining(FI, min_threshold=MinimumThreshold)
print("Frequent Itemsets:\n", FI)
print("\n\n")
print("RuleSet:\n", RuleSet.head)
print("\n\n")



# CFI
# Charm
print("Charm")
MinimumSupport = 0.1
MinimumThreshold = 1
MinimumItemsetLength = 1

print("Minimum Support -", MinimumSupport)
print("Minimum Threshold -", MinimumThreshold)
print("Minimum Itemset Length -", MinimumItemsetLength)

CFI = algo.Charm(Dataset_TE, min_support=MinimumSupport, min_itemset_length=MinimumItemsetLength)
# RuleSet = RuleMining(CFI, min_threshold=MinimumThreshold)
print("Closed Frequent Itemsets:")
cfi_index = 1
for cfi in CFI:
    print(str(cfi_index) + ":", " - ".join(cfi))
    cfi_index += 1
print("\n\n")
# print("RuleSet:\n", RuleSet.head)
print("\n\n")

# AClose
print("AClose")
MinimumSupport = 0.1
MinimumThreshold = 1
MinimumItemsetLength = 1

print("Minimum Support -", MinimumSupport)
print("Minimum Threshold -", MinimumThreshold)
print("Minimum Itemset Length -", MinimumItemsetLength)

CFI = algo.AClose(Dataset_TE, min_support=MinimumSupport, min_itemset_length=MinimumItemsetLength)
# RuleSet = RuleMining(CFI, min_threshold=MinimumThreshold)
print("Closed Frequent Itemsets:")
cfi_index = 1
for cfi in CFI:
    print(str(cfi_index) + ":", " - ".join(cfi))
    cfi_index += 1
print("\n\n")
# print("RuleSet:\n", RuleSet.head)
print("\n\n")

# MFI
# Pincer Search
print("Pincer Search")
MinimumSupport = 0.1
MinimumThreshold = 1
MinimumItemsetLength = 1

print("Minimum Support -", MinimumSupport)
print("Minimum Threshold -", MinimumThreshold)
print("Minimum Itemset Length -", MinimumItemsetLength)

MFI = algo.PincerSearch(Dataset_TE, min_support=MinimumSupport, min_itemset_length=MinimumItemsetLength)
# RuleSet = RuleMining(MFI, min_threshold=MinimumThreshold)
print("Maximal Frequent Itemsets:")
mfi_index = 1
for mfi in MFI:
    print(str(mfi_index) + ":", " - ".join(mfi))
    mfi_index += 1
print("\n\n")
# print("RuleSet:\n", RuleSet.head)
print("\n\n")

# Mafia

print("Mafia")
MinimumSupport = 0.1
MinimumThreshold = 1
MinimumItemsetLength = 1

print("Minimum Support -", MinimumSupport)
print("Minimum Threshold -", MinimumThreshold)
print("Minimum Itemset Length -", MinimumItemsetLength)

MFI = algo.Mafia(Dataset_TE, min_support=MinimumSupport, min_itemset_length=MinimumItemsetLength)
# RuleSet = RuleMining(MFI, min_threshold=MinimumThreshold)
print("Maximal Frequent Itemsets:")
mfi_index = 1
for mfi in MFI:
    print(str(mfi_index) + ":", " - ".join(mfi))
    mfi_index += 1
print("\n\n")
# print("RuleSet:\n", RuleSet.head)
print("\n\n")

# LFI
# Apriori Based LFI
print("Apriori Based LFI")
MinimumSupport = 0.1
MinimumThreshold = 1

print("Minimum Support -", MinimumSupport)
print("Minimum Threshold -", MinimumThreshold)

LFI = algo.AprioriLFI(Dataset_TE, min_support=MinimumSupport)
# RuleSet = RuleMining(LFI, min_threshold=MinimumThreshold)
print("Longest Frequent Itemsets:")
lfi_index = 1
for lfi in LFI:
    print(str(lfi_index) + ":", " - ".join(lfi))
    lfi_index += 1
print("\n\n")
# print("RuleSet:\n", RuleSet.head)
print("\n\n")

# FPGrowth Based LFI
print("FPGrowth Based LFI")
MinimumSupport = 0.1
MinimumThreshold = 1

print("Minimum Support -", MinimumSupport)
print("Minimum Threshold -", MinimumThreshold)

LFI = algo.FPGrowthLFI(Dataset_TE, min_support=MinimumSupport)
# RuleSet = RuleMining(LFI, min_threshold=MinimumThreshold)
print("Longest Frequent Itemsets:")
lfi_index = 1
for lfi in LFI:
    print(str(lfi_index) + ":", " - ".join(lfi))
    lfi_index += 1
print("\n\n")
# print("RuleSet:\n", RuleSet.head)
print("\n\n")

# - Part A - FIM Algos ------------------------------------------------------------------------------------------------

# - Part B - Rules Mining ------------------------------------------------------------------------------------------------
print("- Part B - Rules Mining ------------------------------------------------------------------------------------------------")
RuleSet = algo.RuleMining(FI, min_threshold=MinimumThreshold)
print("RuleSet:\n", RuleSet.head)
print("\n\n")

# - Part B - Rules Mining ------------------------------------------------------------------------------------------------

# - Part C - Predictive Analytics ------------------------------------------------------------------------------------------------
print("- Part C - Predictive Analytics ------------------------------------------------------------------------------------------------")
# Decision Tree
print("Decision Tree on balance-scale dataset:")

Dataset_Path = 'balance-scale.csv'

print("\n\n")

# Building Phase
Dataset = dt.ImportDataset(Dataset_Path)
X, Y, X_train, X_test, Y_train, Y_test = dt.SplitDataset(Dataset)
DT_Gini = dt.Train_Gini(X_train, Y_train)
DT_Entropy = dt.Train_Entropy(X_train, Y_train)

print("\n\n")
    
# Operational Phase
# Prediction using Gini
print("Results Using Gini Index:")
Y_pred_Gini = dt.Predict(X_test, DT_Gini)
dt.PrintAccuracy(Y_test, Y_pred_Gini)

print("\n\n")

# Prediction using Entropy
print("Results Using Entropy:")
Y_pred_Entropy = dt.Predict(X_test, DT_Entropy)
dt.PrintAccuracy(Y_test, Y_pred_Entropy)

print("\n\n")

# Bayes Classifier
print("\n\n")
print("Bayes Classifier on Iris dataset:")

# Building Phase
Dataset = bc.ImportDataset_Iris()
X, Y, X_train, X_test, Y_train, Y_test = bc.SplitDataset(Dataset)
BayesClassifier = bc.Train(X_train, Y_train)

print("\n\n")

# Operational Phase
# Prediction using Gini
print("Results Using Bayes Classifier:")
Y_pred = bc.Predict(BayesClassifier, X_test)
bc.PrintAccuracy(Y_test, Y_pred)

print("\n\n")

# - Part C - Predictive Analytics ------------------------------------------------------------------------------------------------