from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb+srv://<username><password>@score.f3dsl.mongodb.net/?retryWrites=true&w=majority&appName=score")
    # client = MongoClient('mongodb://localhost:27017/')
    db = client.get_database('fantanosize_db')
    return db
