'''
(6) On a given day (average basis), a student is observed to spend 
33% of time in studying, 
30% in sleeping, 
18% in playing, 
5% for hobby activities, 
and rest for spending with friends and family. 
Plot a pie chart showing his daily activities. 
'''
import matplotlib.pyplot as plt
plt.rcdefaults()

def GeneratePieChart(data, labels):
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'grey']
    plt.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()

# Driver Code
data = [33, 30, 18, 5, 14]
labels = ['Study', 'Sleep', 'Play', 'Hobby', 'Friend & Family']

GeneratePieChart(data, labels)