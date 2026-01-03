import os
import sys
import json
import pymongo
import pandas as pd
from dotenv import load_dotenv

from src.exception.exception import CustomerChurnException
from src.logging.logger import logging
from src.entity.config_entity import DATABASE_NAME, COLLECTION_NAME

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class CustomerDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomerChurnException(e,sys)
        
    def csv_to_json_converter(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise CustomerChurnException(e,sys)
    
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)

            return len(self.records)
        except Exception as e:
            raise CustomerChurnException(e,sys)
        
if __name__ == "__main__":
    file_path = "Customer_Data/Churn_Modelling.csv"
    churnobj = CustomerDataExtract()
    records = churnobj.csv_to_json_converter(file_path=file_path)
    print(records)
    no_of_records = churnobj.insert_data_mongodb(records=records,database=DATABASE_NAME,collection=COLLECTION_NAME)
    print(no_of_records)