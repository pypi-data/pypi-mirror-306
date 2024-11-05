from django.conf import settings
from pymongo import MongoClient


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # db_url = "mongodb://phlox:6GlbaXu0sJWUG@143.110.171.18:27017/PhloxLogDatabase?authSource=admin"
    db_url = settings.MONGODB_LOGGER_URL

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(db_url)
    database = settings.APP_NAME.lower()

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[database]


# # This is added so that many files can reuse the function get_database()
# if __name__ == "__main__":
#     # Get the database
#     dbname = get_database()