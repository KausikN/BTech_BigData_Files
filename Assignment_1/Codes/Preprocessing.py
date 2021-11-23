'''
Preprocessing Functions
 - Open CSV as Pandas Dataframe
 - Visualise Data
    -   Print
    -   Mean, Median, Mode
    -   Charts - Pie, Bar, Histogram
 - Transform Data
    -   Encoding of Text as Indices
 - Clean Data
    -   Visualise NULL values
    -   Fill null spaces or indicate null or remove if necc
'''
# Imports
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from tqdm import tqdm

# Main Functions

# Read Data
def ReadCSVFile(filepath):
    return pd.read_csv(filepath)

# Write Data
def WriteCSVFile(Data, filepath):
    return Data.to_csv(filepath, index=False)
    
# Visualise Data

# Print Data
def PrintData(Data):
    print(Data)

# Charts
# 1
def Histogram(Data, nbins=25, xlabel="X Axis", ylabel="Y Axis", title="Histogram"):
    n, bins, patches = plt.hist(Data, nbins, facecolor='blue', alpha=0.5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def PieChart(Data, labels, colors=['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'grey']):
    plt.pie(Data, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()

def BarGraph(Data, labels, xlabel="X Axis", ylabel="Y Axis", title="Bar Graph"):
    plt.bar(Data, Data, align='center', alpha=0.5)
    plt.xticks(Data, labels)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

# 2
def BoxPlot(Data, xlabel="X Axis", ylabel="Y Axis", title="Box Plot"):
    plt.boxplot(Data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def ViolinPlot(Data, title="Violin Plot"):
    plt.violinplot(Data)
    plt.title(title)
    plt.show()

# 3
def StemPlot(Stems, Leaves, xlabel="X Axis", ylabel="Y Axis", title="Box Plot"):
    plt.title('Stem and Leaf Plot')
    plt.xlabel('Stems')
    plt.ylabel('Leaves')
    markerline, stemlines, baseline = plt.stem(Stems, Leaves)
    plt.show()

def DensityPlot(Data, labels, xlabel="X Axis", ylabel="Y Axis", title="Density Plot"):
    for x, label in zip(Data, labels):
        sns.distplot(x, hist = False, kde = True,
                    kde_kws = {'linewidth': 3},
                    label = label)
    
    # Plot formatting
    plt.legend(prop={'size': 16}, title = title)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def RugPlot(Data, labels, xlabel="X Axis", ylabel="Y Axis", title="Rug Plot"):
    for x, label in zip(Data, labels):
        sns.rugplot(x, label=label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def SwarmPlot(Data, xlabel="X Axis", ylabel="Y Axis", title="Swarm Plot"):
    sns.swarmplot(Data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def JitteredBoxPlot(Data, xlabel="X Axis", ylabel="Y Axis", title="Jittered Box Plot"):
    sns.boxplot(data=Data)
    sns.swarmplot(data=Data, color='grey')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def RadarPlot_PlotLY(statsList, labels):
    for stats in statsList:
        df = pd.DataFrame(dict(r=stats, theta=labels))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.show()

def FunnelPlot(Data, labels):
    data = dict(number=Data, stage=labels)
    fig = px.funnel(data, x='number', y='stage')
    fig.show()



# Transform Data
def EncodeDataset(Dataset):
    Dataset_Transformed = Dataset.copy()
    LabelIndexMaps = {}

    for k in Dataset.keys():
        Dataset_Transformed[k], LabelIndexMaps[k] = EncodeData(Dataset[k])

    return Dataset_Transformed, LabelIndexMaps

def EncodeData(Data):
    Data_Transformed = []
    LabelIndexMap = []

    # Get Label to Index Map and Transform Data
    curIndex = 0
    for x in Data:
        if not x in LabelIndexMap:
            # Add to Map
            curIndex = len(LabelIndexMap)
            LabelIndexMap.append(x)
            # Transform
            Data_Transformed.append(curIndex)
        else:
            Data_Transformed.append(LabelIndexMap.index(x))

        # if not x in LabelIndexMap.keys():
        #     # Add to Map
        #     LabelIndexMap[x] = curIndex
        #     # Transform
        #     Data_Transformed.append(curIndex)
        #     curIndex += 1
        # else:
        #     Data_Transformed.append(LabelIndexMap[x])
        
    return Data_Transformed, LabelIndexMap


# Clean Data
# Visualise data to clean
def Mode(X):
    modex = -1
    modex_freq = -1

    freq = FreqDist(X)

    for key in freq.keys():
        if freq[key] > modex_freq:
            modex = key
            modex_freq = freq[key]

    return modex

def FreqDist_BinWise(X, binsize):
    values = []
    Freq = {}
    minVal = int(min(X))
    maxVal = int(round(max(X)))
    print("Range:", minVal, "-", maxVal)
    for i in range(minVal, maxVal+1, binsize):
        values.append(i)
        Freq[str(i)] = 0
    for x in X:
        key = int(int((round(x) - minVal)/binsize)*binsize + minVal)
        Freq[str(key)] += 1
    return Freq

def FreqDist(X):
    Freq = {}
    for x in X:
        if x in Freq.keys():
            Freq[x] += 1
        else:
            Freq[x] = 1
    return Freq

def PrintNonZeroFreq(FreqDist, binsize):
    print("Freq Dist Non Zero Values: ")
    nbins = 0
    for k in FreqDist.keys():
        if FreqDist[k] > 0:
            nbins += 1
            #print(k, ":", FreqDist[k], "\n")
    print("Found", nbins, "non empty bins")

def MissingCount(Data):
    missing = 0
    indices = []
    i = 0
    for d in Data:
        if CheckMissing(d):
            missing += 1
            indices.append(i)
        i += 1
    return missing, indices

# Cleaning Functions
def MissingClean(Dataset, NotReplacable_Keys = ["Symbol", "Scientific Name with Author"], NoChange_Keys = ["Synonym Symbol"], Replacable_Keys = ["National Common Name", "Family"]):
    Dataset_MissingCleaned = {}
    for key in Dataset.keys():
        Dataset_MissingCleaned[key] = []
    ListDicts = Dataset.T.to_dict().values() # Convert Dataframe to list of dicts

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

    n_removed = 0
    n_replaced = 0

    mode = ''
    for data in tqdm(ListDicts):
        data_cleaned = {}
        nullData = False # If any non replacable field is null
        replacedData = False # If replacable key data has already been replaced
        for key in data.keys():
            if key in NotReplacable_Keys:
                mode = 'remove'
                if CheckMissing(data[key]):
                    nullData = True
                    break
                else:
                    data_cleaned[key] = data[key]
            elif key in NoChange_Keys:
                mode = 'nochange'
                if CheckMissing(data[key]):
                    data_cleaned[key] = "NULLVALUE"
                else:
                    data_cleaned[key] = data[key]
            elif key in Replacable_Keys and not replacedData:
                mode = 'replace'
                # Check for subset in Scientific Name with Author if data is missing
                if CheckMissing(data[key]):
                    data[key] = "NULLVALUE"
                    for data_subs in ListDicts:
                        if data['Scientific Name with Author'] in data_subs['Scientific Name with Author']:
                            for rep_key in Replacable_Keys:
                                if CheckMissing(data[rep_key]):
                                    data_cleaned[rep_key] = data_subs[rep_key]
                                else:
                                    data_cleaned[rep_key] = data[rep_key]
                            replacedData = True
                            break
                else:
                    data_cleaned[key] = data[key]

        if not nullData:
            for key in data.keys():
                Dataset_MissingCleaned[key].append(data_cleaned[key])
            if replacedData:
                n_replaced += 1
        else:
            n_removed += 1

    Dataset_MissingCleaned = pd.DataFrame.from_dict(Dataset_MissingCleaned)

    return Dataset_MissingCleaned, n_removed, n_replaced
        
def RedundantClean(Dataset):
    Dataset_RedundantCleaned = {}
    for key in Dataset.keys():
        Dataset_RedundantCleaned[key] = []
    ListDicts = Dataset.T.to_dict().values() # Convert Dataframe to list of dicts

    # Dataset also contains some repeated data rows
    # Basic Cleaning - Search for duplicate data rows and remove all duplicates
    # IN THIS DATASET DONT DO - Advanced Cleaning - Remove row even if it is a subset of the data of any other row - REDUNDANT

    n_duplicates = 0

    # Remove Repeated Rows
    uniqList = []
    for data in tqdm(ListDicts):
        if not data in uniqList:
            uniqList.append(data)
            for key in Dataset_RedundantCleaned.keys():
                Dataset_RedundantCleaned[key].append(data[key])
        else:
            n_duplicates += 1

    Dataset_RedundantCleaned = pd.DataFrame.from_dict(Dataset_RedundantCleaned)

    return Dataset_RedundantCleaned, n_duplicates


# Util Functions
def SplitDict(Dict):
    keys = Dict.keys()
    data = []
    for k in keys:
        data.append(Dict[k])
    return data, keys

def CheckMissing(Val):
    if str(Val).strip().replace('nan', '') in ['', ' ', 'NULL', 'null'] or 'NaN' in str(Val):
        return True
    return False

'''
# Driver Code
dataset_path = 'Assignment 1/Dataset.csv'
Dataset = ReadCSVFile(dataset_path)

# Print Dataset
print("Dataset Row Count:", len(Dataset['Symbol']))
print("Dataset: 5 rows: ")
print(Dataset.head(n=5))

print("\n\n")

# Vis Freq of Dataset
print("Dataset Freq Visualistion...")
print("Number of unique entries:")
for key in Dataset.keys():
    Freq = FreqDist(Dataset[key])
    data, labels = SplitDict(Freq)
    print(key, "-", len(labels))
    #print(key, ":\n", FreqDist(Dataset[key]), "\n\n")
    #BarGraph(data, labels)

print("\n\n")

# Vis Missing Dataset
print("Missing Count:")
for key in Dataset.keys():
    missing, indices = MissingCount(Dataset[key])
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
Dataset_MissingCleaned, n_removed, n_replaced = MissingClean(Dataset)
print("\n")
print("Removed", n_removed, "data rows")
print("Replaced", n_replaced, "data rows")
print("\n")
print("Cleaned Dataset Missing Count:")
for key in Dataset.keys():
    missing, indices = MissingCount(Dataset[key])
    print(key, "-", missing)

print("\n\n")

# REDUNDANT DATA CLEAN
# Dataset also contains some repeated data rows
# Basic Cleaning - Search for duplicate data rows and remove all duplicates
# Advanced Cleaning - Remove row even if it is a subset of the data of any other row - REDUNDANT - IN THIS DATASET DONT DO

Dataset_RedundantCleaned, n_duplicates = RedundantClean(Dataset_MissingCleaned)
print("\n")
print("Removed", n_duplicates, "duplicate data rows")
print("\n")
print("Redundant Cleaned Dataset Row Count:", len(Dataset_RedundantCleaned['Symbol']))

print("\n\n")

# Final Cleaned Dataset
Dataset_Cleaned = Dataset_RedundantCleaned

# Save Cleaned Dataset
WriteCSVFile(Dataset_Cleaned, 'Assignment 1/Dataset_Cleaned.csv')

# Encode Dataset
print("Encoding Dataset...")
Data_Transformed, LabelIndexMaps = EncodeDataset(Dataset_Cleaned)
print("Encoded Dataset: 5 Rows:")
print(Data_Transformed.head(n=5))
#print(LabelIndexMaps)

# Save Encoded Dataset
WriteCSVFile(Data_Transformed, 'Assignment 1/Dataset_Cleaned_Encoded.csv')
pickle.dump(LabelIndexMaps, open('Assignment 1/LabelIndexMaps.p', 'wb'))

# Visualise Preprocessed Data - Family Distribution
Histogram(Data_Transformed['Family'], len(LabelIndexMaps['Family']), 'Family Name', 'Frequency', 'Family Frequency')

print("\n\n")
'''