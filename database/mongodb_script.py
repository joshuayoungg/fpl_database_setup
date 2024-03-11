from pymongo import MongoClient
from decouple import config
from pymongo.server_api import ServerApi
import configparser

config = configparser.ConfigParser()


def __get_creds():
    config.read('creds.ini')
    username = config['CREDS']['username']
    password = config['CREDS']['password']
    return (username, password)


def __get_connection():
    print('Connecting to database..')
    username, password = __get_creds()
    uri = 'mongodb+srv://{username}:{password}@epl.oysq8wl.mongodb.net/?retryWrites=true&writeConcern=majority'.format(
        username=username, password=password)
    client = MongoClient(uri, server_api=ServerApi('1'))
    print('Connection Established!')
    return client


def __add_to_mongo(client, items):
    db = client.epl
    for item in items:
        collection = db[item[0]]
        try:
            collection.drop()
            collection.insert_many(item[1])
        except Exception as e:
            print('Error occurred inserting into ', item[0], ', error: ', e)
            return
    print("Added items successfully!")


def mongo_db_operations(operation, items=None):
    if items is None:
        return
    try:
        client = __get_connection()
    except Exception as e:
        print("Error occurred connecting: ", e)
        return
    if operation == "add":
        print('Adding items...')
        __add_to_mongo(client, items)
    client.close()
