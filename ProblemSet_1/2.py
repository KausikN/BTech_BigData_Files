'''
(2) In a class of 18 students, assume marks distribution in an exam are as follows. 
Let the roll numbers start with CSE20D01 and all the 
odd roll numbers secure marks as follows: 25+((i+7)%10) and 
even roll numbers : 25+((i+8)%10).  
Develop an application that sets up the data  and calculate the mean and median for the marks obtained using the platform support.
'''

def GenerateMarks(n_students, rollno_prefix):
    marks = []
    rollnos = []
    for i in range(n_students):
        zero_prefix = '0' * (len(str(n_students)) - len(str(i)))
        rollno = rollno_prefix + zero_prefix + str(i)
        mark = 0
        if i % 2 == 0:
            mark = 25 + ((i + 8) % 10)
        else:
            mark = 25 + ((i + 7) % 10)
        marks.append(mark)
        rollnos.append(rollno)
    return marks, rollnos

def Mean(marks):
    sum = 0
    for mark in marks:
        sum += mark
    return sum / len(marks)

def Median(marks):
    BubbleSort(marks)

    if len(marks) % 2 == 1:
        return marks[int((len(marks) - 1)/2)]
    else:
        return (marks[int(len(marks)/2)] + marks[int(len(marks)/2 - 1)]) / 2

def BubbleSort(arr):
    n = len(arr)

    # Traverse through all array elements
    for i in range(n):
 
        # Last i elements are already in place
        for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]

# Driver Code
n_students = int(input("Enter no of students: "))
rollno_prefix = 'CSE20D'
marks, rollnos = GenerateMarks(n_students, rollno_prefix)
print("Marks: ")
i = 0
for mark, rollno in zip(marks, rollnos):
    print(str(i+1) + ":", rollno, "-", mark)
    i += 1
print("Mean Marks:", Mean(marks))
print("Median Marks:", Median(marks))