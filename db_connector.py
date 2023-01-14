import os
import logging
import random
import pymongo
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

MONGO_CONNECTION_STRING = os.environ.get("MONGO_CONNECTION_STRING")
client = None
db = None
collection = None


def connect_to_db():
    global client, db, collection
    try:
        logger.info("Connecting to the database...")
        client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
        db = client["cs_glossary"]
        collection = db["cs_glossary"]
    except pymongo.errors.ConnectionFailure as err:
        logger.error("Error connecting to the database...", exc_info=True)
        raise


def fetch_random_term():
    try:
        if not client:
            connect_to_db()
        logger.info("Fetching random term...")
        count = collection.count_documents({'posted': False})
        if count > 0:
            random_term = collection.aggregate([{'$match': {'posted': False}}, {'$sample': {'size': 1}}])
            random_term = list(random_term)[0]
            term = random_term['term']
            definition = random_term['definition']
            return term, definition
        else:
            logger.info("No more terms to post, updating all terms to posted...")
            if update_all_posted():
                return fetch_random_term()
            else:
                raise Exception("Something terrible has happened...")
    except Exception as err:
        logger.error("Error fetching random term...", exc_info=True)
        raise


def update_posted(term):
    try:
        if not client:
            connect_to_db()
        logger.info("Updating term...")
        collection.update_one({'term': term}, {"$set": {"posted": True}})
        logger.info("Term updated...")
    except Exception as err:
        logger.error("Error updating term to posted...", exc_info=True)
        raise


def update_all_posted():
    try:
        if not client:
            connect_to_db()
        result = collection.update_many({}, {"$set": {"posted": False}})
        print(f"Updated count: {result.modified_count}")
        return True
    except Exception as err:
        logger.error("Error updating all terms to posted...", exc_info=True)
        raise
