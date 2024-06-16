from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

'''
FN -> fetch_documents

return dict:
 {status: boolean, data : list (of jsons), error : str, code : str}

possible error codes:
    DBE : DATABSE ERROR
'''

'''
FN -> insert_document

return dict:
 {status: boolean, data : str, error : str, code : str}

possible error codes:
    DBE : DATABSE ERROR
'''

'''
FN -> delete_document

return dict:
 {status: boolean, data : str, error : str, code : str}

possible error codes:
    DDE : DOCUMENT DELTE ERROR
'''

def insert_document(database_name, collection_name, document):
    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
        id =collection.insert_one(document).inserted_id

        client.close()
        return {"status" : True, "data" : id, "error" : "", "code" : ""}
    except Exception as e:
        print("mongo module threw except", e)
        return {"status" : False, "data" : "", "error" : str(e), "code" : "DBE"}

def fetch_documents(database_name, collection_name, query):
    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
        documents = list(collection.find(query))
        client.close()
        return {"status" : True, "data" : documents, "error" : "", "code" : ""}
    except Exception as e:
        {"status" : False, "data" : "", "error" : str(e), "code" : "DBE"}

def delete_collection(database_name, collection_name):
    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
        collection.drop()
        return {"status" : True, "data" : "", "error" : "", "code" : ""}
    except Exception as e:
        {"status" : False, "data" : "", "error" : str(e), "code" : "DBE"}

def delete_document(db, collection, query):
    try:
        client = MongoClient(mongo_uri)
        db = client[db]
        collection = db[collection]
        collection.delete_one(query)
        client.close()
        return {"status" : True, "data" : "", "error" : "", "code" : ""}
    except Exception as e:
        {"status" : False, "data" : "", "error" : str(e), "code" : "DDE"}

def update_document(database_name, collection_name, id_field, id_value, field_to_update, value_to_update):
    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
        query = {id_field : id_value}
        new_values = { "$set": {field_to_update: value_to_update} }
        collection.update_one(query, new_values)
        return {"status" : True, "data" : "", "error" : "", "code" : ""}
    except Exception as e:
        {"status" : False, "data" : "", "error" : str(e), "code" : "DBE"}

def replace_document(database_name, collection_name, doc_id, new_document):
    try:
        new_document['_id'] = doc_id

        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]

        # Attempt to replace the document
        result = collection.replace_one({"_id": doc_id}, new_document)
        
        client.close()

        # Check if a document was replaced
        if result.matched_count:
            return {"status": True, "data": str(doc_id), "error": "", "code": ""}
        else:
            return {"status": False, "data": "", "error": "No document found with the provided _id", "code": "DBE"}

    except Exception as e:
        return {"status": False, "data": "", "error": str(e), "code": "DBE"}