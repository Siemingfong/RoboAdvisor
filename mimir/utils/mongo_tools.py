from mimir import MONGO_CLIENT

def get_mongo_db(db_name):
    return MONGO_CLIENT[db_name]