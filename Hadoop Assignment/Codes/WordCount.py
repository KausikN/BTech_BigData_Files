'''
Word Count using PySpark
'''

# Imports
# import findspark
# findspark.init()
import pyspark
import sys
from pyspark import SparkContext, SparkConf

# Main Functions
def InitSpark():
    # Creating a spark context
    return SparkContext("local", "PySpark Word Count Program")

def ReadWordsFromFile(sc, path):
    # Read Words in Input File
    return sc.textFile(path).flatMap(lambda line: line.split(" "))

def WordCount_Spark(words):
    # Count Occurence of each word
    return words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

def SaveData(wordCounts, savePath):
    if not savePath == None:
        # Save data as text file
        wordCounts.saveAsTextFile(savePath)

def PrintData(wordCounts):
    # Print Counts
    print("Word Counts:\n", wordCounts.collect())

# Driver Code
# Params
inputPath = 'wordCountInput.txt'
savePath = None

# Init Spark
sc = InitSpark()

# Read Words and count
words_data = ReadWordsFromFile(sc, inputPath)
word_counts = WordCount_Spark(words_data)

# Save and Print
SaveData(word_counts, savePath)
PrintData(word_counts)