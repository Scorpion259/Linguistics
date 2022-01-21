from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb+srv://ScorpionVSTU:VsTuBoY@scorpioncluster.kb9vl.mongodb.net/ling?retryWrites=true&w=majority')
db = client['ling']
articles_collection = db['news']

all_articles = articles_collection.find({})[:1000]
print(all_articles)


@app.route('/')
def index():
    all_articles = articles_collection.find({})[:1000]
    return render_template('basic_table.html', title='Ling', users=all_articles)


if __name__ == '__main__':
    app.run()
