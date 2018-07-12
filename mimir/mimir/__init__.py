from mimir.settings import *
import pymongo
from pymongo.errors import *
from urllib.parse import quote_plus
MONGO_CLIENT = []
try:
    """
    uri = "mongodb://%s:%s@%s:%s/%s" % (
        quote_plus(MONGO_USER), 
        quote_plus(MONGO_PASSWORD), 
        quote_plus(MONGO_HOST),
        quote_plus(str(MONGO_PORT)),
        quote_plus(MONGO_NAME)
        )
    """
    uri = "mongodb://localhost:27017/"
    print("uri", uri)
    client = pymongo.MongoClient(uri)
except OperationFailure as err:
    print(f"User {settings.MONGO_USER} connect {settings.MONGO_HOST} failed!")
    print("Error ", err)