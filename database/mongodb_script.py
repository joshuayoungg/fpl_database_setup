# TODO: Update mongodb script to follow new api changes
from pymongo import MongoClient
from decouple import config
from pymongo.server_api import ServerApi
import configparser

config = configparser.ConfigParser()


def __get_creds():
    config.read('creds.ini')
    username = config['CREDS']['username']
    password = config['CREDS']['password']
    return(username, password)


def __get_connection():
    username, password = __get_creds()
    uri = 'mongodb+srv://{username}:{password}@epl.oysq8wl.mongodb.net/?retryWrites=true&writeConcern=majority'.format(
        username=username, password=password)
    client = MongoClient(uri, server_api=ServerApi('1'))
    print('Connection Established!')
    return client


def __add_to_mongo(client, items = None):
    db = client.epl
    # collection = db.gameweek_stats
    # collection.drop()
    # collection.insert_many(items)
    collection = db.teams
    collection.drop()
    collection.insert_many(items[0])
    collection = db.players
    collection.drop()
    collection.insert_many(items[1])

def __get_from_mongo(client):
    db = client.epl
    collection = db.teams
    items = collection.find()
    new_items = []
    for item in items:
        new_items.append(item)
    return new_items


def mongo_db_operations(operation, items=None):
    try:
        client = __get_connection()
        if operation == "add":
            print('Adding items...')
            __add_to_mongo(client, items)
            print("Added items to collection")
        elif operation == "get":
            print('Getting Data..')
            items = __get_from_mongo(client)
        client.close()
        return items
    except Exception as e:
        print("Error occurred: ", e)
