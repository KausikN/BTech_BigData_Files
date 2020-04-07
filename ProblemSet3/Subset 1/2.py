'''
2. Use the given dataset and perform the operations listed below. 
Dataset Description It is a well-known fact that Millenials LOVE Avocado Toast. 
It's also a well known fact that all Millenials live in their parents basements. 
Clearly, they aren't buying home because they are buying too much Avocado Toast! But maybe there's hope... 
if a Millenial could find a city with cheap avocados, they could live out the Millenial American Dream. 
Help them to filter out the clutter using some pre-processing techniques. 
Some relevant columns in the dataset: 
• Date - The date of the observation 
• AveragePrice - the average price of a single avocado 
• type - conventional or organic 
• year - the year 
• Region - the city or region of the observation 
• Total Volume - Total number of avocados sold 
• 4046 - Total number of avocados with PLU* 4046 sold 
• 4225 - Total number of avocados with PLU* 4225 sold 
• 4770 - Total number of avocados with PLU* 4770 sold (Product Lookup codes (PLU’s)) * 

a. 
Sort the attribute “Total Volume” in the dataset given and distribute the data into equal sized/frequency bins of size 50 & 250.
Smooth the sorted data by  
(i)bin-means 
(ii) bin-medians 
(iii) bin-boundaries (smooth using bin boundaries after trimming the data by 2%). 

b. 
The dataset represents weekly retail scan data for National retail volume (units) and price. 
Retail scan data comes directly from retailers’ cash registers based on actual retail sales of Hass avocados. 
However, the company is interested in the monthly (total per month) and annual sales (total per year), rather than the total per week. 
So, reduce the data accordingly. 

c.
Summarize the number of missing values for each attribute  

d.
Populate data for the missing values of the attribute= “Average Price” by averaging their values that fall under the same region. 

e. 
Discretize the attribute=“Date” using concept hierarchy into {Old, New, Recent} {2015,2016 : Old, 2017: New, 2018: Recent} and plot in q-q plots 
'''
import pandas as pd
import numpy as np
import statsmodels.api as sm 
import pylab as py

def ReadCSVFile(filepath):
    return pd.read_csv(filepath)

def FreqDist(X, binsize):
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

def PrintNonZeroFreq(FreqDist, binsize):
    print("Freq Dist " + str(binsize) + " Non Zero Values: ")
    nbins = 0
    for k in FreqDist.keys():
        if FreqDist[k] > 0:
            nbins += 1
            #print(k, ":", FreqDist[k], "\n")
    print("Found", nbins, "non empty bins")

def MissingCount(Data, label):
    missing = 0
    indices = []
    i = 0
    for d in Data[label]:
        if str(d).strip().replace('nan', '') in ['', ' '] or 'NaN' in str(d):
            missing += 1
            indices.append(i)
        i += 1
    return missing, indices

# Driver Code
filepath = 'ProblemSet3/Subset 1/avocado_csv.csv'
labels = ['Unnamed: 0', 'Date', 'AveragePrice', 'Total Volume', '4046', '4225',
            '4770', 'Total Bags', 'Small Bags', 'Large Bags', 'XLarge Bags', 'type',
            'year', 'region']
Data = ReadCSVFile(filepath)

# A
FreqDist50 = FreqDist(Data['Total Volume'], 50)
FreqDist250 = FreqDist(Data['Total Volume'], 250)
PrintNonZeroFreq(FreqDist50, 50)
PrintNonZeroFreq(FreqDist250, 250)

# B

# C
print("Missing Counts:")
for label in labels:
    miscount = MissingCount(Data, label)
    print(label, miscount)

# D
MissingLabel = 'AveragePrice'
missingcount, indices = MissingCount(Data, MissingLabel)
Data_NoMissing = Data.copy()
for i in indices:
    Region = Data_NoMissing['region'][i]
    AvgP = 0.0
    RegionCount = 0
    for a, r in zip(Data_NoMissing[MissingLabel], Data_NoMissing['region']):
        if r == Region and a not in ['', ' ', 'nan'] and '.' in str(a):
            AvgP += float(a)
            RegionCount += 1
    AvgP /= RegionCount
    Data_NoMissing[MissingLabel][i] = str(AvgP)
    print("Added Value", AvgP, "to missing value in region", Region)
print("Now missing count:", MissingCount(Data_NoMissing, MissingLabel))

# E
# DateLabels = [2015,2016 : 'Old', 2017: 'New', 2018: 'Recent']
DateLabels = ['Old', 'New', 'Recent']
DateIndices = {}
DateValues = {}
for l in DateLabels:
    DateIndices[l] = []
    DateValues[l] = []
for di in range(len(Data['Date'])):
    date = Data['Date'][di].split('-')
    if date[2] in ['2015', '2016']:
        DateIndices['Old'].append(di)
        #DateValues['Old'].append(Data['Date'][di])
        DateValues['Old'].append(int(date[0]) + int(date[1])*30)
    elif date[2] in ['2017']:
        DateIndices['New'].append(di)
        #DateValues['New'].append(Data['Date'][di])
        DateValues['New'].append(int(date[0]) + int(date[1])*30)
    elif date[2]in ['2018']:
        DateIndices['Recent'].append(di)
        #DateValues['Recent'].append(Data['Date'][di])
        DateValues['Recent'].append(int(date[0]) + int(date[1])*30)
print("Dicretized Date Sizes:")
for l in DateLabels:
    print(l, len(DateIndices[l]))
    sm.qqplot(np.array(DateValues[l]), line ='45') 
    py.show() 
