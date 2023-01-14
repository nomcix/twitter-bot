import os
import csv
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_CONNECTION_STRING = os.environ.get("MONGO_CONNECTION_STRING")

client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client["cs_glossary"]
collection = db["cs_glossary"]
documents = []

with open('data/first_50.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        document = {
            'term': row[0],
            'definition': row[1],
            'posted': False
        }
        documents.append(document)


collection.insert_many(documents)