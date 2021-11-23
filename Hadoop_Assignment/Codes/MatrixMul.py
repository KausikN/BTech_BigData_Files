'''
Matrix Multiplication using PySpark
'''

# Imports
# import findspark
# findspark.init()
import numpy as np
from pyspark.mllib.linalg.distributed import RowMatrix
from pyspark.mllib.linalg.distributed import *
from pyspark import SparkContext
from pyspark.sql.session import SparkSession

# Main Functions
def InitSpark():
    # Creating a sparkcontext and sparksession
    sc = SparkContext("local", "PySpark Matrix Multiplier Program")
    spark = SparkSession(sc)
    return spark, sc

def GenerateRandomMatrix(size, valRange=(0, 100)):
    # Create Random Matrix
    M = np.random.randint(valRange[0], valRange[1], size).astype(np.float64)
    # M = np.arange(1024 ** 2, dtype=np.float64).reshape(1024, 1024)
    return M

def toBlockMatrix(rdd, rowsPerBlock=1024, colsPerBlock=1024):
    # Convert array into blockmatrix
    return IndexedRowMatrix(rdd.zipWithIndex().map(lambda xi: IndexedRow(xi[1], xi[0]))).toBlockMatrix(rowsPerBlock, colsPerBlock)

def MatrixMultiply_Spark(sc, A, B):
    # Matrix Multiply using Spark
    bm_A = toBlockMatrix(sc.parallelize(A))
    bm_B = toBlockMatrix(sc.parallelize(B))
    return (bm_A.multiply(bm_B)).toLocalMatrix()

def MatrixMultiply_Numpy(A, B):
    # Matrix Multiply using Numpy
    return A.dot(B)

# Driver Code
# Params
size = (1024, 1024)
valRange = (1, 101)

# Init Spark
spark, sc = InitSpark()

# Generate Random Matrices
A = GenerateRandomMatrix(size, valRange)
B = GenerateRandomMatrix(size, valRange)
print("A:\n", A, "\n")
print("B:\n", B, "\n")

# Multiply using Spark
product_Spark = MatrixMultiply_Spark(sc, A, B)
print("Spark Product:\n", product_Spark, "\n")

# Multiply using Numpy
product_Numpy = MatrixMultiply_Numpy(A, B)
print("Numpy Product:\n", product_Numpy, "\n")