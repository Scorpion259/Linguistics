from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from pymongo import MongoClient
from progress.bar import IncrementalBar
import os
import time


tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)

CONNECTION_STRING = "mongodb+srv://ScorpionVSTU:VsTuBoY@scorpioncluster.kb9vl.mongodb.net/ling?retryWrites=true&w=majority"

client = MongoClient(CONNECTION_STRING)
db = client.ling
collection = db.sentence
data_list = collection.find()
sentences = []
for row in data_list:
    sentences.append(row['sentence'])

results = model.predict(sentences, k=2)
tonality = ''
clear = lambda: os.system('clear')
bar = IncrementalBar('Countdown', max=len(sentences))
for message, sentiment in zip(sentences, results):
    result = '; '.join([f'{key.capitalize()}: {value}' for key, value in sentiment.items()])
    collection.update_one({'sentence': message}, {'$set': {'tonality': result}})
    clear()
    bar.next()
    time.sleep(0.1)
bar.finish()