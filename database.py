from pymongo import MongoClient
from dotenv import load_dotenv
import os
# import ssl

load_dotenv()


def ConnectToDB(collName):
    CONNECTION_STRING = os.environ.get("CONNECTION_STRING")
    client = MongoClient(CONNECTION_STRING)
    mydb = client['Discord-CompanionDB']
    collection = mydb[collName]
    return collection


def fetch(collName: str):
    coll = ConnectToDB(collName)
    document = list(coll.find({}))
    return document, coll


def InsertScan(scan: dict, victimUsername: str):
    doc, coll = fetch(victimUsername)
    result = coll.insert_many(scan)
    return result


def InsertUserIfNotFound(collection, user, datetime_inserted):
    # collection.find_one({"pk": user["pk"]})
    # print(user)
    # print(isFound)
    if(collection.find_one({"pk": user["pk"]}) is None):
        user['datetime_inserted'] = datetime_inserted
        resp = collection.insert_one(user)
        if(resp.inserted_id):
            print(f"username: {user['username']}")
            return True
        else:
            print(f"FAILED TO INSERT DOCUMENT: {user}")
            return False
