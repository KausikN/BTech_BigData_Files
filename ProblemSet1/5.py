'''
(5) In Analytics and Systems of Bigdata course, for a class of 100 students, 
around 31 students secured ‘S’ grade, 
29 secured ‘B’ grade,  
25 ‘C’ grades, and 
rest of them secured ‘D’ grades.  
If the range of each grade is 15 marks. 
(S for 85 to 100 marks, A for 70 to 85 …). 
Develop an application that represents the above data : using Pie and Bar graphs.
'''
import matplotlib.pyplot as plt
plt.rcdefaults()

def GeneratePieChart(data, labels):
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'grey']
    plt.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()

def GenerateBarGraph(data, labels):
    plt.bar(data, data, align='center', alpha=0.5)
    plt.xticks(data, labels)
    plt.xlabel('Grades')
    plt.ylabel('No of Students')
    plt.title('Class Performance')
    plt.show()

# Driver Code
data = [31, 0, 29, 25, 15]
labels = ['S', 'A', 'B', 'C', 'D']

GenerateBarGraph(data, labels)
GeneratePieChart(data, labels)