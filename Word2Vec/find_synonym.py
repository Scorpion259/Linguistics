from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2VecModel
from pyspark.sql import DataFrame

MODEL_PATH = "model"

spark = SparkSession \
    .builder \
    .appName("word2vec") \
    .getOrCreate()

model = Word2VecModel.load(MODEL_PATH)
count = 5

while(True):
    try:
        word = input("Введите слово из словаря: ")
        if(word == "exit"):
            break
        else:
            model.findSynonyms(word, count).show(n=count)
    except Exception as ex:
        print("Данного слова нет в словаре!")

spark.stop()