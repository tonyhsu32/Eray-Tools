from contextlib import ExitStack
from pymongo import MongoClient, errors
from pymongo import InsertOne, UpdateOne, UpdateMany
from pymongo.errors import BulkWriteError, ConnectionFailure
import json
import time
import sys
import os
import re
import gc

folder_path = "/home/eray/Documents/xml_2_json/mongo_db/obj_info_data"

# define mongo client parameters
LOCALHOST = "127.0.0.1"   # "127.0.0.1", "192.168.33.157"
PORT = 27017
AUTH_USER = "root"
AUTH_PWD = "80661707"

DB_NAME = ["eraydb", "test_db", "obj_info_db"]
DB_COLLECTION = ["eray_data", "test_data", "info_data"]


class Mongo_Client:
    def __init__(self, host, port, db_name, db_collection, db_user, db_pwd):
        self.localhost = host
        self.port = port
        self.db_user = db_user
        self.db_pwd = db_pwd

        self.select_db = db_name
        self.db_collection = db_collection
       
    def set_db(self):
        try:
            param_wrap = {"host": self.localhost, 
                          "port": self.port,
                          "username": self.db_user, 
                          "password": self.db_pwd, 
                        #   "authSource": "admin",
                        #   "authMechanism": 'SCRAM-SHA-1', # 'SCRAM-SHA-256'
                          "serverSelectionTimeoutMS": 3000}

            client = MongoClient(**param_wrap)
            print("Connected Success!")

        except ConnectionFailure as e:
            print(f"Server Error: {e}")

        db = client[self.select_db] 
        db_col = db[self.db_collection]

        return db, db_col


def file_generator(dir_path):
    count = 0
    pattern = re.compile(".json$")

    with ExitStack() as stack:
        for f in os.listdir(dir_path):
            if re.search(pattern, f):
                # path = os.path.join(dir_path, f)
                try:
                    file = stack.enter_context(open(os.path.join(dir_path, f)))
                    
                except OSError as e:
                    # print(e)
                    stack.close()
                    file = stack.enter_context(open(os.path.join(dir_path, f)))
                
                finally:
                    json_file = json.load(file)

                    yield json_file
                    count += 1
                    print(f"iterator files: ------> {os.path.join(dir_path, f)}")
                    
            else:
                print(f"{os.path.join(dir_path, f)} not a json file !")
                continue
       
                
def insert_multi_json(input_path, db_collection):
    try:
        # method 1: (bulk_write)
        num = 0

        if db_collection.estimated_document_count() > 0:
            # db_collection.bulk_write([UpdateOne(f, {"$set": f}, upsert = True) for f in file_generator(input_path)])
            for f in file_generator(input_path):
                # db_collection.bulk_write([UpdateOne(f, {"$set": f}, upsert = True)])
                db_collection.bulk_write([UpdateMany(f, {"$set": f}, upsert = True)])
                num += 1

        else:
            # db_collection.bulk_write([InsertOne(f) for f in file_generator(input_path)])
            for f in file_generator(input_path):
                db_collection.bulk_write([InsertOne(f)])
                num += 1
        
        # method 2: (insert_many)
        # files = [f for f in file_generator(dir_path)]
        # db_collection.insert_many(files)

        # method 3: (insert_one)
        # count = 0
        # for file in file_generator(dir_path):
        #     db_content.insert_one(file)
        #     count += 1  

    except BulkWriteError as bwe:
        print(bwe.details)
    
    print(f"Insert < {num} document > to {DB_NAME[2]} ! \n")
    print(f"Total: < {db_collection.estimated_document_count()} document > in {DB_NAME[2]} ! \n")
    # print(f"f_stack memory used: {(sys.getsizeof(files) / 1024):.2f} mb")

    # del files
    gc.collect()

    # print(f"Insert < {count} dict > to eraydb ! \n")
    

if __name__ == "__main__":
    s = time.time()
    _, db_set = Mongo_Client(LOCALHOST, PORT, DB_NAME[2], DB_COLLECTION[2], AUTH_USER, AUTH_PWD).set_db()

    insert_multi_json(folder_path, db_set)
    e = time.time()

    print(f"Spent {e-s:.2f} seconds !")
   
    
   
