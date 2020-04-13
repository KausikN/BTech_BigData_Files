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
#from functools import lru_cache
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
def OneHotEncoder(Dataset):
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

def GenerateMFCS(MFCS, Items_Si):		#For Pincer Search Algorithm
    MFCS = MFCS.copy()

    for inf_items in Items_Si:
        for MFCS_item in MFCS.copy():
            # print(MFCS_item)
            #if infrequent is subset of MFCS
            if all(s_item in MFCS_item for s_item in inf_items):
                MFCS.remove(MFCS_item)

                for item in inf_items:
                    updateMFCS_item = MFCS_item.copy()
                    updateMFCS_item.remove(item)

                    if not any(all(s_item in Rem_MFCS for s_item in updateMFCS_item) for Rem_MFCS in MFCS):
                        MFCS.append(updateMFCS_item)
    return MFCS

# @lru_cache(maxsize=32)
def compVertBitmap(itemset, bitMap):
    if len(itemset) == 1:
        item = str(itemset[0])
        return bitMap[item]

    else:
        last_item = str(itemset[-1])
        return compVertBitmap(itemset[:-1], bitMap) & bitMap[last_item]

def countSupp(itemset, bitMap):
	
    # VerticalBitmap(itemset, bitMap)
    itemset_map = compVertBitmap(itemset, bitMap)
    itemset_supp_count = np.count_nonzero(itemset_map)
    # print(itemset_supp_count)
    return itemset_supp_count

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

# MFI
# Pincer Search
def PincerSearch(Dataset_Encoded, min_support=0.05, min_itemset_length=1):
    MFI = []

    min_support = min_support * len(Dataset_Encoded.index)
    print("Minimum Support:", min_support)

    ListDicts = Dataset_Encoded.T.to_dict().values() # Convert Dataframe to list of dicts

    Items = Dataset_Encoded.keys()
    ItemCounts = []

    MFCS = [[items] for items in Items]

    Items_Li = []
    Items_Si = []
    i = 1

    Items_Ci = [[item] for item in Items]

    while(len(Items_Ci) > 0):
        
        # Count Supports of Items_Ci and MFCS
        ItemCounts = [0] * len(Items_Ci)
        for data in ListDicts:
            for i in range(len(Items_Ci)):
                ItemPresent = True
                for val in Items_Ci[i]:
                    if data[val] == False:
                        ItemPresent = False
                        break
                if ItemPresent:
                    ItemCounts[i] += 1
        
        MFCSCount = [0] * len(MFCS)
        for data in ListDicts:
            for i in range(len(MFCS)):
                ItemPresent = True
                for val in MFCS[i]:
                    if data[val] == False:
                        ItemPresent = False
                        break
                if ItemPresent:
                    MFCSCount[i] += 1


        #Update MFI: MFI U freqitems in MFCS
        for itemset, support in zip(MFCS, MFCSCount):
            if ((support >= min_support) and (itemset not in MFI)):
                MFI.append(itemset)
        
        # Infrequent sets
        Items_Li = []
        Items_Si = []
        for item, count in zip(Items_Ci, ItemCounts):
            if count >= min_support:
                Items_Li.append(item)
            else:
                Items_Si.append(item)
        #update MFCS
        MFCS = GenerateMFCS(MFCS, Items_Si)
        
        # Prune LK that are subsets of MFI
        Ck = Items_Ci.copy()
        for item in Items_Ci.copy():
            if any(all(s_item in MFIitem for s_item in item) for MFIitem in MFI):
                Ck.remove(item)
        Items_Li = Ck

        i += 1
        # Self-Join
        Items_Ci = SelfJoin(Items_Li, sizelimit=i)

        #Prune Ck+1 that are not in MFCS
        Ck = Items_Ci.copy()
        for item in Items_Ci.copy():
            if not any(all(s_item in MFCSitem for s_item in item) for MFCSitem in MFCS):
                Ck.remove(item)
        Items_Ci = Ck

    return MFI

# Mafia
class MafiaTree:
    def __init__(self, head, tail, supportCount=None):	# supportCount=None
        self.head = head
        self.tail = tail.copy()
        self.supportCount = supportCount

def MafiaRun(currentMFNode, MFI, bitMap, Items, transCount, min_support):
    #Head Union Tail Pruning (HUT)------>
    HUT = currentMFNode.head + tuple(currentMFNode.tail)
    # HUT = currentMFNode.head.append(currentMFNode.tail)

    #If HUT is in MFI -> Stop Searching nd return
    if any(all(item in mfi for item in HUT) for mfi in MFI):
        return MFI

    #Count Support of all children
    # print('--------------------------------------',currentMFNode.head)
    nodeChild_supportCount = [(item, countSupp(currentMFNode.head + (item,), bitMap) ) for item in currentMFNode.tail]
    # nodeChild_supportCount = [(item, countSupp(currentMFNode.head.append(item), bitMap) ) for item in currentMFNode.tail]
    #Extract frequent Children of node and support count
    nodeFreqChildCount = [(item, support_count) for item, support_count in nodeChild_supportCount if support_count >= min_support]

    node_childEqualParent = []	# items in tail with support count equal to that of parent
    node_tail_suppCount = []	# items in node tail sorted by Decreasing Support

    for item, support_count in nodeFreqChildCount:
        if support_count == currentMFNode.supportCount:
            node_childEqualParent.append(item)
        else:
            node_tail_suppCount.append((item, support_count))

    #Sort items in the trimmed tail by increasing support:
    node_tail_suppCount.sort(key=lambda x:x[1])
    node_tail_items = [item for item, support in node_tail_suppCount]

    currentMFNode.head += tuple(node_childEqualParent)
    # currentMFNode.head.append(node_childEqualParent)
    currentMFNode.tail = node_tail_items

    is_leaf = not bool(currentMFNode.tail)

    for i, item in enumerate(currentMFNode.tail):
        new_node_head = currentMFNode.head + (item,)
        # new_node_head.append(item)
        new_node_tail = currentMFNode.tail[i+1:]
        new_node_supportCount = node_tail_suppCount[i][1]

        new_node = MafiaTree(new_node_head, new_node_tail, new_node_supportCount)

        MFI = MafiaRun(new_node, MFI, bitMap, Items, transCount, min_support)

    if is_leaf and currentMFNode.head and not any(all(item in mfi for item in currentMFNode.head) for mfi in MFI):
        MFI.append(set(currentMFNode.head))

    return MFI

def Mafia(Dataset_Encoded, min_support=0.05, min_itemset_length=1):
    MFI = []

    min_support = min_support * len(Dataset_Encoded.index)
    print("Minimum Support:", min_support)

    Items = Dataset_Encoded.keys()
    Itemlist = []
    for item in Items:
        Itemlist.append(item)
    transCount, itemCount = Dataset_Encoded.shape
    # print(transCount)
    items_vertical_bitmaps = {item:np.array(Dataset_Encoded[item]) for item in Items}

    root = tuple()
    MFRoot = MafiaTree(root, Itemlist)	#Creates a root Node 

    MFI = MafiaRun(MFRoot, MFI, items_vertical_bitmaps, Itemlist, transCount, min_support)

    return MFI

# LFI
# Apriori Based LFI
def AprioriLFI(Dataset_Encoded, min_support=0.05):
    LFI = []

    # Run apriori and get all frequent itemsets
    FreqItemsets = Apriori(Dataset_Encoded, min_support=min_support)
    #print(FreqItemsets['itemsets'])

    # Convert to list of itemsets 2d array
    FI = []
    for itemset in FreqItemsets['itemsets']:
        FI.append(list(itemset))

    # Search and find the longest itemset
    max_len = 0
    for fi in FI:
        if len(fi) == max_len:
            LFI.append(fi)
        elif len(fi) > max_len:
            LFI = []
            LFI.append(fi)
            max_len = len(fi)

    return LFI

# FPGrowth Based LFI
def FPGrowthLFI(Dataset_Encoded, min_support=0.05):
    LFI = []

    # Run FPGrowth and get all frequent itemsets
    FreqItemsets = FPGrowth(Dataset_Encoded, min_support=min_support)
    #print(FreqItemsets['itemsets'])

    # Convert to list of itemsets 2d array
    FI = []
    for itemset in FreqItemsets['itemsets']:
        FI.append(list(itemset))

    # Search and find the longest itemset
    max_len = 0
    for fi in FI:
        if len(fi) == max_len:
            LFI.append(fi)
        elif len(fi) > max_len:
            LFI = []
            LFI.append(fi)
            max_len = len(fi)

    return LFI

'''
# Driver Code
dataset_path = 'Assignment 1/Dataset_Cleaned.csv'
#LabelIndexMap_path = 'Assignment 1/LabelIndexMaps.p'

Dataset_Preprocessed = ReadCSVFile(dataset_path)
#LabelIndexMap = pickle.load(open(LabelIndexMap_path, 'rb'))

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
Dataset_TE = OneHotEncoder(Dataset_Preprocessed.head(Dataset_PortionSize))

print("\n\n")

# FIM
# Apriori
print("Apriori")

MinimumSupport = 0.1
MinimumThreshold = 1

print("Minimum Support -", MinimumSupport)
print("Minimum Threshold -", MinimumThreshold)

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

print("Minimum Support -", MinimumSupport)
print("Minimum Threshold -", MinimumThreshold)

FI = FPGrowth(Dataset_TE, min_support=MinimumSupport)
RuleSet = RuleMining(FI, min_threshold=MinimumThreshold)
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

CFI = Charm(Dataset_TE, min_support=MinimumSupport, min_itemset_length=MinimumItemsetLength)
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

CFI = AClose(Dataset_TE, min_support=MinimumSupport, min_itemset_length=MinimumItemsetLength)
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

MFI = PincerSearch(Dataset_TE, min_support=MinimumSupport, min_itemset_length=MinimumItemsetLength)
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

MFI = Mafia(Dataset_TE, min_support=MinimumSupport, min_itemset_length=MinimumItemsetLength)
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

LFI = AprioriLFI(Dataset_TE, min_support=MinimumSupport)
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

LFI = FPGrowthLFI(Dataset_TE, min_support=MinimumSupport)
# RuleSet = RuleMining(LFI, min_threshold=MinimumThreshold)
print("Longest Frequent Itemsets:")
lfi_index = 1
for lfi in LFI:
    print(str(lfi_index) + ":", " - ".join(lfi))
    lfi_index += 1
print("\n\n")
# print("RuleSet:\n", RuleSet.head)
print("\n\n")
'''