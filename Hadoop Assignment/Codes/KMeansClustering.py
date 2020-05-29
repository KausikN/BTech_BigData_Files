'''
K-Means Clustering using PySpark
'''

# Imports
# import findspark
# findspark.init()
from pyspark.sql.functions import split
from pyspark.ml.clustering import KMeans
from pyspark import SparkContext, since
from pyspark.sql import SQLContext as sc
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.ml.feature import VectorAssembler

# Main Functions
def InitSpark():
    # Creating spark context and starting a session
    sc = SparkContext.getOrCreate()
    spark = SparkSession(sc)
    return spark, sc

def ReadTextFile(path):
    # Read Input Data
    return sc.textFile(path)

def GenerateFeatureLists(text_lines):
    # Create Features from Text Data - Skip 1st attribute
    features = []
    for line in text_lines.collect():
        l = str(line)
        feature_list = line.split()
        feature_list = feature_list[1 : :]
        features.append(list(map(lambda x: int(x), feature_list)))
    return features

def CreateSparkDataframe(spark, features):
    # Generate Column names
    colNames = []
    for i in range(len(features[0])):
        colNames.append("A_" + str(i))

    # Creating Dataframe of features
    return spark.createDataFrame(features, colNames), colNames

def VectorAssembleData(df, colNames):
    # Vector Assemble Data to make it compatible with KMeans
    vecAssembler = VectorAssembler(inputCols=colNames, outputCol="features")
    return vecAssembler.transform(df)

def KMeans_InitModel(k=5, seed=1):
    # Aliasing the inbuild KMeans function as kmeans with number of clusters 5 and seed as 1 (random initial points)
    return KMeans(k=k, seed=seed)

def KMeans_FitModel(model, df_va):
    # Fit Model to data
    return model.fit(df_va.select('features'))

def TransformData(model, df_va, colNames):
    # Drop all Initial Columns and transform to feature vectors with cluster
    transformed = model.transform(df_va)
    # for name in colname:
    # transformed.drop(name).collect()
    return transformed.drop(*colNames)

def PrintData(model):
    # Printing the centers of the clusters
    print("The Centres are : ")
    for centre in model.clusterCenters():
        print(centre)

# Driver Code
# Params
path = 'pumsb.dat'
k = 5
seed = 1

# Init Spark
spark, sc = InitSpark()

# Read Input File
text_data = ReadTextFile(path)

# Generate Feature Lists and Create Spark Dataframe and Vector Assemble Transform data
features = GenerateFeatureLists(text_data)
print("The total number of data points are : ", len(features))

df, colNames = CreateSparkDataframe(spark, features)
print("Column Names:\n", colNames)
print("Initial Dataframe:\n", df.show())

df_va = VectorAssembleData(df, colNames)
print("VectorAssembleTransformed Dataframe:\n", df_va.show())

# Use KMeans
model = KMeans_InitModel(k=k, seed=seed)
model = KMeans_FitModel(model, df_va)
df_transformed = TransformData(model, df_va, colNames)
print("Final Transformed Dataframe:\n", df_transformed.show())

# Print Data
PrintData(model)