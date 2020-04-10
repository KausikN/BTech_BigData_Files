'''
Implementation of Algorithms
FIM - Apriori, FPGrowth
CFI - Charm, AClose
MFI - Mafia, Pincer Search
'''
# Imports
import pickle
import numpy as np
import pandas as pd
from tqdm import tqdm
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import apriori, fpgrowth
from mlxtend.preprocessing import TransactionEncoder

import Preprocessing

# Main Functions
# Read Data
def ReadCSVFile(filepath):
    return pd.read_csv(filepath)
    
# Write Data
def WriteCSVFile(Data, filepath):
    return Data.to_csv(filepath, index=False)

# Visualise Data

# Describe Data
def DescribeDataset(Dataset):
    for key in Dataset.keys():
        print("Column:", key)
        print("N Unique Values:", len(Dataset[key].unique()))
    print("\n\n")
    print("Dataset:")
    print(Dataset.head)

# Util Functions
def TransactionalEncoder(Dataset):
    # TE = TransactionEncoder()
    # TE_Arr = TE.fit(Dataset).transform(Dataset)
    # return pd.DataFrame(TE_Arr, columns=TE.columns_)
    Dataset_Encoded = []
    ListDicts = Dataset.T.to_dict().values() # Convert Dataframe to list of dicts

    UniqueValues, UniqueValKeys = GetUniqueValues(Dataset)

    for data in tqdm(ListDicts):
        EncodedData = []
        for val, key in zip(UniqueValues, UniqueValKeys):
            if val == data[key]:
                EncodedData.append(True)
            else:
                EncodedData.append(False)
        Dataset_Encoded.append(EncodedData)
    
    Dataset_Encoded = pd.DataFrame(Dataset_Encoded, columns=UniqueValues)

    return Dataset_Encoded

def GetUniqueValues(Dataset):
    UniqueValues = []
    UniqueValKeys = []
    for key in Dataset.keys():
        uniquevals = Dataset[key].unique()
        for uv in uniquevals:
            if uv not in UniqueValues:
                UniqueValues.append(uv)
                UniqueValKeys.append(key)
    return UniqueValues, UniqueValKeys

def SelfJoin(Set, sizelimit=None):
    JoinedSet = []
    JoinedSetDicts = []

    for i in range(len(Set)):
        for j in range(i+1, len(Set)):
            val = {}
            for x, y in zip(Set[i], Set[j]):
                val[x] = True
                val[y] = True
            if sizelimit == None or sizelimit >= len(val.keys()):
                if val not in JoinedSetDicts:
                    JoinedSetDicts.append(val)
                    JoinedSet.append(list(val.keys()))
            
    return JoinedSet

            

# Algorithms

# FIM
# Apriori
def Apriori(Dataset_Encoded, min_support=0.05):
    # Build apriori model
    FrequentItems = apriori(Dataset_Encoded, min_support=min_support, use_colnames=True)
    return FrequentItems
    
# FPGrowth
def FPGrowth(Dataset_Encoded, min_support=0.05):
    FrequentItems = fpgrowth(Dataset_Encoded, min_support=min_support, use_colnames=True)
    return FrequentItems

# RuleSet Mining
def RuleMining(FrequentItems, min_threshold=1):
    # Collect the inferred rules
    RuleSet = association_rules(FrequentItems, metric ="lift", min_threshold=min_threshold)
    RuleSet = RuleSet.sort_values(['confidence', 'lift'], ascending=[False, False])
    return RuleSet

# CFI
# Charm
def Charm(Dataset_Encoded, min_support=0.05, min_itemset_length=1):
    CFI = []

    min_support = min_support * len(Dataset_Encoded.index)
    print("Minimum Support:", min_support)

    # Procedure
    # Minimum Support - 3
    # Count A(4), B(6), C(4), D(4), E(5) as supports
    Items = Dataset_Encoded.keys()
    ItemCounts = []
    for item in Items:
        ItemCounts.append(sum(Dataset_Encoded[item]))
    
    # Write in Ascending order of Support
    # A, C, D, E, B
    Items_Sorted = Items.copy()
    ItemCounts_Sorted = ItemCounts.copy()
    sorted_list1 = [y for _,y in sorted(zip(ItemCounts_Sorted,Items_Sorted),key=lambda x: x[0])]
    sorted_list2 = sorted(ItemCounts_Sorted)
    Items_Sorted = sorted_list1
    ItemCounts_Sorted = sorted_list2

    # Then write transactions where it occurs
    # A - 1, 3, 4, 5
    # C - 2, 4, 5, 6
    # D - 1, 3, 5, 6
    # E - 1, 2, 3, 4, 5
    # B - 1, 2, 3, 4, 5, 6
    AppearanceDict = {}
    for item in Items_Sorted:
        AppearanceDict[item] = [i for i, val in enumerate(Dataset_Encoded[item]) if val]

    # Make Pairs
    # For A and C - common trans - 4, 5 - count 2 < MinSupp = 3
    # As < MinSupp DONT COUNT THAT PAIR
    # A and D - 1, 3, 5 - count = 3 = 3 - TAKE A and D as pair
    # Now a new thing called AD with trans - 1, 3, 5
    # Now compare AD with E - AD - 135 subset of 12345 - E
    # As subset Cancel AD and make it as ADE
    # Now again check ADE with B - ADE - 135 subset of 123456 - B
    # As subset cancel ADE make it ADEB
    # As no further items after B - ADEB is first closed freq itemset
    # 
    # Next Check A with E - 1345 (A) is subset if 12345 (E)
    # So, replace A with AE
    # Check AE with B - 1345 is subset of 123456 (E)
    # Replace AE with AEB - No further - AEB is CFI
    #
    # Next Check C with D
    # No subset but common items are 5, 6 - count 2 < MinSup - DONT TAKE
    # C and E - common - 245 - count 3 = MinSupp
    # Now new thing CE has ele 245
    # CE with B - 245 is subset of 123456 (B)
    # So replace CE with CEB - as no further - CEB is CFI
    #
    # Next Check C with B - subset - CB is CFI
    # 
    # And So On
    for i in tqdm(range(len(Items_Sorted))):
        cfi_item = [Items_Sorted[i]]
        cfi_available = False
        for j in range(i+1, len(Items_Sorted)):
            CommonElements = [value for value in AppearanceDict[Items_Sorted[i]] if value in AppearanceDict[Items_Sorted[j]]]
            CommonCount = len(CommonElements)
            if CommonCount >= min_support:
                cfi_item = [Items_Sorted[i], Items_Sorted[j]]
                # Not Sure if needed Subset or Common Elements

                # Common Elements
                # for k in range(j+1, len(Items_Sorted)):
                #     CommonElements_temp = [value for value in CommonElements if value in AppearanceDict[Items_Sorted[k]]]
                #     CommonCount_temp = len(CommonElements_temp)
                #     if CommonCount_temp >= min_support:
                #         CommonElements = CommonElements_temp
                #         CommonCount = CommonCount_temp
                #         cfi_item.append(Items_Sorted[k])

                # Subset
                for k in range(j+1, len(Items_Sorted)):
                    if set(CommonElements).issubset(set(AppearanceDict[Items_Sorted[k]])):
                        CommonElements = AppearanceDict[Items_Sorted[k]]
                        CommonCount = len(AppearanceDict[Items_Sorted[k]])
                        cfi_item.append(Items_Sorted[k])
                
                if min_itemset_length <= len(cfi_item):
                    CFI.append(cfi_item)
                cfi_available = True
        if not cfi_available and min_itemset_length <= 1:
            if len(AppearanceDict[Items_Sorted[i]]) >= min_support:
                cfi_item = [Items_Sorted[i]]
                CFI.append(cfi_item)

    return CFI

# AprioriClose - AClose
def AClose(Dataset_Encoded, min_support=0.05, min_itemset_length=1):
    CFI = []

    min_support = min_support * len(Dataset_Encoded.index)
    print("Minimum Support:", min_support)

    ListDicts = Dataset_Encoded.T.to_dict().values() # Convert Dataframe to list of dicts

    # Count Items
    Items = Dataset_Encoded.keys()
    ItemCounts = []
    for item in Items:
        ItemCounts.append(sum(Dataset_Encoded[item]))
    
    # Prune Level 1
    Items_L1 = []
    ItemCounts_L1 = []
    for item, count in zip(Items, ItemCounts):
        if count >= min_support:
            Items_L1.append([item])
            ItemCounts_L1.append(count)

    # Keep Pruning Till Empty
    Items_Li = Items_L1
    ItemCounts_Li = ItemCounts_L1
    i = 1
    while(len(Items_Li) > 0):
        i += 1

        # Add previous Values to CFI if superset and remove subsets
        newCFI = CFI.copy()
        for item in Items_Li:
            for cfi in CFI:
                if set(cfi).issubset(set(item)): # Check if subset
                    if cfi in newCFI:
                        newCFI.remove(cfi)
            if min_itemset_length <= len(item):
                newCFI.append(item)
                    # CFI.remove(cfi)
            # if min_itemset_length <= len(item):
                # CFI.append(item)
        CFI = newCFI

        # Self-Join
        Items_Ci = SelfJoin(Items_Li, sizelimit=i)

        # Count Supports of Items_Ci
        ItemCounts = [0] * len(Items_Ci)
        for data in ListDicts:
            for i in range(len(Items_Ci)):
                ItemPresent = True
                for val in Items_Ci[i]:
                    if not data[val]:
                        ItemPresent = False
                        break
                if ItemPresent:
                    ItemCounts[i] += 1
                
        
        # Prune
        Items_Li = []
        for item, count in zip(Items_Ci, ItemCounts):
            if count >= min_support:
                Items_Li.append(item)
    
    return CFI






# Driver Code
dataset_path = 'Assignment 1/Dataset_Cleaned.csv'
LabelIndexMap_path = 'Assignment 1/LabelIndexMaps.p'

Dataset_Preprocessed = ReadCSVFile(dataset_path)
LabelIndexMap = pickle.load(open(LabelIndexMap_path, 'rb'))

# Print Dataset
DatasetRowCount = len(Dataset_Preprocessed['Symbol'])
print("Dataset Row Count:", DatasetRowCount)
print("Dataset: 5 rows: ")
print(Dataset_Preprocessed.head(n=5))

print("\n")

# Encode Dataset
DatasetPortionPercentage = 0.005
Dataset_PortionSize = int(DatasetPortionPercentage * DatasetRowCount)
if Dataset_PortionSize > DatasetRowCount:
    Dataset_PortionSize = DatasetRowCount
print("Operating on", Dataset_PortionSize, " data rows.")
print("Encoding...")
Dataset_TE = TransactionalEncoder(Dataset_Preprocessed.head(Dataset_PortionSize))

print("\n\n")
'''
# FIM
# Apriori
print("Apriori")

MinimumSupport = 0.1
MinimumThreshold = 1

FI = Apriori(Dataset_TE, min_support=MinimumSupport)
RuleSet = RuleMining(FI, min_threshold=MinimumThreshold)
print("Frequent Itemsets:\n", FI)
print("\n\n")
print("RuleSet:\n", RuleSet.head)
print("\n\n")

# FPGrowth
print("FPGrowth")
MinimumSupport = 0.1
MinimumThreshold = 1

FI = FPGrowth(Dataset_TE, min_support=MinimumSupport)
RuleSet = RuleMining(FI, min_threshold=MinimumThreshold)
print("Frequent Itemsets:\n", FI)
print("\n\n")
print("RuleSet:\n", RuleSet.head)
print("\n\n")
'''
# CFI
# Charm
print("Charm")
MinimumSupport = 0.1
MinimumThreshold = 1
MinimumItemsetLength = 1

CFI = Charm(Dataset_TE, min_support=MinimumSupport, min_itemset_length=MinimumItemsetLength)
# RuleSet = RuleMining(FrequentItems, min_threshold=MinimumThreshold)
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

CFI = AClose(Dataset_TE, min_support=MinimumSupport, min_itemset_length=MinimumItemsetLength)
# RuleSet = RuleMining(FrequentItems, min_threshold=MinimumThreshold)
print("Closed Frequent Itemsets:")
cfi_index = 1
for cfi in CFI:
    print(str(cfi_index) + ":", " - ".join(cfi))
    cfi_index += 1
print("\n\n")
# print("RuleSet:\n", RuleSet.head)\
print("\n\n")

# MFI
# Mafia
