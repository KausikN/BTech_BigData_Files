'''
Given the following setup {Class,Tally score, Frequency}, develop an application that generates the table shown 
(you can populate the relevant data ; minimum data size :50 records). 
The table is only an illustration for a data of color scores, 
you are free to test the application over any data set with the application generating the tally and frequency scores.
'''
import random

def GenerateTallyStr(no):
    five = '||||\\ '
    tally = five * int(no / 5) + '|' * (no % 5)
    return tally

def FreqDist(X):
    # Accepts only 1, 2, 3, other
    freq = {}
    freq['1'] = 0
    freq['2'] = 0
    freq['3'] = 0
    freq['other'] = 0
    for x in X:
        if x in [1, 2, 3]:
            freq[str(x)] += 1
        else:
            freq['other'] += 1
    return freq

# Driver Code
Data = []
it = 20
for i in range(it):
    Data.append(random.randint(1, 5))
classes = ['1', '2', '3', 'other']
freq = FreqDist(Data)

print("Score\t\t", "Tally\t\t", "Frequency")
for c in classes:
    print(c + "\t\t", GenerateTallyStr(freq[c]) + "\t\t", str(freq[c]))
