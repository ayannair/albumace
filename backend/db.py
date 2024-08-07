from pymongo import MongoClient

# Function to get the MongoDB client and database
def get_db():
    client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
    db = client['fantanosize_db']  # Replace with your database name
    return db
