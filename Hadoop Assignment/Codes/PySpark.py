'''
PySpark Functions
'''

# Imports
from pyspark import SparkConf, SparkContext
import sys

# Main Functions
def multiply(row):

    multiply_row = []
    for i in row:
        for j in row:
            multiply = float(i) *float(j)
            multiply_row.append(multiply)
    return multiply_row

def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

def sum_values(a, b):
    return tuple(sum(x) for x in zip(a,b))

def MatrixMultiply():
    conf = SparkConf().setAppName('MatrixMultiplier')
    sc = SparkContext(conf=conf)
    assert sc.version >= '1.5.1'

    raw_matrix_file = sc.textFile(sys.argv[1])
    # Read matrix from file and split the lines based on space and use float for items
    matrix = raw_matrix_file.map(lambda line: line.split()).map(lambda value: [float(i) for i in value])

    Col = matrix.take(1)

    nCol = [len(x)for x in Col]
    # doing purmutation on the row by row for example a b = aa ab ba bb

    # doing the sum coloumn by coloumn
    row_permutation = matrix.map(lambda row: multiply(row)).reduce(sum_values)

    matrix_chunks = chunks(row_permutation,nCol[0])

    # open a file to write the matrix output on local and write in required format
    filelocation = sys.argv[2]

    t_file = open(filelocation, 'w')
    i =1
    for num in row_permutation:
        if(i % nCol[0] == 0):
            t_file.write("%s" % num + "\n")

        else:
            t_file.write("%s" % num + " ")
        i = i+1

# below lines worte the output in spark format using save as a text file : uncomment if running on cluster
   # matrix_unformated = sc.parallelize(matrix_chunks).coalesce(1)

    #matrix_formated = (matrix_unformated.map(lambda m: ' '.join(map(str, m))))

    #matrix_formated.saveAsTextFile(sys.argv[2])
