'''
(7) Develop an application (absolute grader) that accepts marks scored by 
20 students in ASBD course 
(as a split up of three : 
Mid Sem (30), 
End Sem(50) and 
Assignments(20). 
Compute the total and use it to grade the students following absolute grading :
>=90 – S ; >=80 – A and so on till D. 
Compute the Class average for total marks in the course and 50% of class average would be fixed as the cut off for E. 
Generate a frequency table for the grades as well (Table displaying the grades and counts of them).  
'''
import random

def GenerateData(n_data, rand=True):
    MidSemMarks = []
    EndSemMarks = []
    AssignmentMarks = []
    for i in range(n_data):
        if rand:
            MidSemMarks.append(random.randint(0, 30))
            EndSemMarks.append(random.randint(0, 50))
            AssignmentMarks.append(random.randint(0, 20))
        else:
            MidSemMarks.append(int(input("Enter Midsem Marks for " + str(i+1) + ": ")))
            EndSemMarks.append(int(input("Enter Endsem Marks for " + str(i+1) + ": ")))
            AssignmentMarks.append(int(input("Enter Assignment Marks for " + str(i+1) + ": ")))
    return MidSemMarks, EndSemMarks, AssignmentMarks
        
def CalculateTotalMarks(MidSemMarks, EndSemMarks, AssignmentMarks):
    TotalMarks = []
    for midsem, endsem, assign in zip(MidSemMarks, EndSemMarks, AssignmentMarks):
        TotalMarks.append(midsem + endsem + assign)
    return TotalMarks

def GetGrade(mark, avgmarks):
    grade = 'U'
    if mark >= 90:
        grade = 'S'
    elif mark >= 80:
        grade = 'A'
    elif mark >= 70:
        grade = 'B'
    elif mark >= 60:
        grade = 'C'
    elif mark >= 50:
        grade = 'D'
    elif mark >= int(avgmarks / 2):
        grade = 'E'
    else:
        grade = 'U'
    return grade

def CalculateGrades(TotalMarks):
    Grades = []
    avgmarks = Mean(TotalMarks)
    for totmark in TotalMarks:
        Grades.append(GetGrade(totmark, avgmarks))
    return Grades

def Mean(X):
    sum = 0
    for x in X:
        sum += x
    return sum / len(X)

def FreqDist(X, keys):
    freq = {}
    for key in keys:
        freq[key] = 0
    for x in X:
        freq[x] = 0
    for x in X:
        freq[x] += 1
    return freq

# Driver Code
n_data = 20
PossibleGrades = ['S', 'A', 'B', 'C', 'D', 'E', 'U']
MidSemMarks, EndSemMarks, AssignmentMarks = GenerateData(n_data, True)
TotalMarks = CalculateTotalMarks(MidSemMarks, EndSemMarks, AssignmentMarks)
Grades = CalculateGrades(TotalMarks)
print("Mean Marks:", Mean(TotalMarks))
print("Grades:")
i = 0
for mark, grade in zip(TotalMarks, Grades):
    i += 1
    print(str(i) + ":", mark, "-", grade)
    
print("Freq Dist of Grades: ")
freq = FreqDist(Grades, PossibleGrades)
for key in PossibleGrades:
    print(key + ":", freq[key])