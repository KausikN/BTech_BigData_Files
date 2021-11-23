'''
Frequent Itemset Mining using PySpark
'''

# Imports
# import findspark
# findspark.init()
from pyspark.sql.functions import split
from pyspark.ml.fpm import FPGrowth
from pyspark import SparkContext, since
from pyspark.sql import SQLContext as sc
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession

# Main Functions
def InitSpark():
    # Creating a spark context and starting a session
    sc = SparkContext.getOrCreate()
    spark = SparkSession(sc)
    return sc, spark

def ReadTextFile(path):
    # Read Input Data
    return sc.textFile(path)

def Data_to_Transactions(text_lines):
    # Convert Data to Transactions
    trans = []
    i = 0
    for line in text_lines.collect():
        trans.append((i, list(set(map(lambda x: int(x), str(line).split())))))
        i = i + 1
    return trans

def CreateSparkDataframe(spark, trans, itemsColName='items'):
    # Create Spark Dataframe
    df = spark.createDataFrame(trans, ["id", itemsColName])
    return df

def FpGrowth_CreateModel(itemsCol='items', minSupport=0.05, minConfidence=0.75):
    # Aliasing the inbuild FPGrowth function as fpgrwoth and setting the minimumsupport to be 0.05 (that is around 50000) and min
    # confidence as 0.75
    return FPGrowth(itemsCol="items", minSupport=0.05, minConfidence=0.75)

def FpGrowth_FitModel(model, df):
    # Fitting our model
    return model.fit(df)

def PrintData(model, df):
    # FI
    print("Frequent Itemsets:")
    print(model.freqItemsets.show())

    # AR
    print("Association Rules:")
    print(model.associationRules.show())

    # Predictions
    print("Predictions for input data:")
    print(model.transform(df).show())

# Driver Code
# Params
path = 'kosarak.dat'
itemsCol = 'items'
minSupport = 0.05
minConfidence = 0.75

# Init Spark
sc, spark = InitSpark()

# Read Input Data
text_data = ReadTextFile(path)

# Transform data to transactions and make dataframe
trans = Data_to_Transactions(text_data)
print("No of Transactions:", len(trans))
df = CreateSparkDataframe(spark, trans, itemsColName=itemsCol)
print("Dataframe:\n", df.show())

# Create and Fit Model to data
model = FpGrowth_CreateModel(itemsCol, minSupport, minConfidence)
model = FpGrowth_FitModel(model, df)

# Display Results
PrintData(model, df)