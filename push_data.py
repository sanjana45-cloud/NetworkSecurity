
import os
import sys
import json

import pymongo
import certifi
import pandas as pd
from dotenv import load_dotenv

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


# Load environment variables from .env file
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_DATA")

# Create MongoDB connection
client = pymongo.MongoClient(MONGO_DB_URL)

try:
    client.admin.command("ping")
    print("MongoDB connection successful!")
except Exception as e:
    print("MongoDB connection failed:", e)


# Get trusted certificate authority
ca = certifi.where()


class NetworkDataExtract():

    def __init__(self):
        try:
            pass

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def cv_to_json_convertor(self, file_path):
        try:
            # Read CSV file
            data = pd.read_csv(file_path)

            # Reset index
            data.reset_index(drop=True, inplace=True)

            # Convert dataframe to JSON records
            records = list(
                json.loads(data.T.to_json()).values()
            )

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):

        try:
            self.database = database
            self.collection = collection
            self.records = records

            # Create MongoDB client
            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=ca
            )

            # Select database
            self.database = self.mongo_client[self.database]

            # Select collection
            self.collection = self.database[self.collection]

            # Insert records
            self.collection.insert_many(self.records)

            return len(self.records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":

    File_path = "Network_Data/phisingData.csv"

    DATABASE = "Sanjanaai"

    Collection = "NetworkData"

    networkobj = NetworkDataExtract()

    # Convert CSV data into records
    records = networkobj.cv_to_json_convertor(
        file_path=File_path
    )

    print("Number of records created:", len(records))

    # Insert records into MongoDB
    no_of_records = networkobj.insert_data_mongodb(
        records,
        DATABASE,
        Collection
    )
    print("Number of records inserted:", no_of_records)