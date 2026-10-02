import os
import sys
import json

import pymongo
import certifi
import pandas as pd
from dotenv import load_dotenv

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging


load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_DATA")

ca = certifi.where()


class NetworkDataExtract:

    def __init__(self):
        try:
            pass

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def cv_to_json_convertor(self, file_path):

        try:

            data = pd.read_csv(file_path)

            data.reset_index(drop=True, inplace=True)

            records = list(
                json.loads(data.T.to_json()).values()
            )

            return records

        except Exception as e:

            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):

        try:

            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=ca
            )

            self.database = self.mongo_client[database]

            self.collection = self.database[collection]

            result = self.collection.insert_many(records)

            print("Database:", database)
            print("Collection:", collection)
            print("Inserted records:", len(result.inserted_ids))

            return len(result.inserted_ids)

        except Exception as e:

            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":

    File_path = "phisingData.csv"

    DATABASE = "Sanjanaai"

    Collection = "NetworkData"

    networkobj = NetworkDataExtract()

    records = networkobj.cv_to_json_convertor(
        file_path=File_path
    )

    print("Number of records created:", len(records))

    no_of_records = networkobj.insert_data_mongodb(
        records,
        DATABASE,
        Collection
    )

    print("Number of records inserted:", no_of_records)