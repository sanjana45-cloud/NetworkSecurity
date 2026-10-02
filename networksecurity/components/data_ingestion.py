import os
import sys

import numpy as np
import pandas as pd
import pymongo
import certifi

from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifacts_entity import DataIngestionArtifact


# Load environment variables
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_DATA")


class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            # Create MongoDB client
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            # Select database and collection
            collection = self.mongo_client[database_name][collection_name]

            # Convert MongoDB collection into DataFrame
            df = pd.DataFrame(list(collection.find()))

            # Remove MongoDB ID column
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            # Replace "na" with NaN
            df.replace({"na": np.nan}, inplace=True)

            logging.info("Data successfully exported from MongoDB")

            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, df: pd.DataFrame):

        try:
            feature_store_file_path = (
                self.data_ingestion_config.feature_store_file_path
            )

            dir_path = os.path.dirname(feature_store_file_path)

            os.makedirs(dir_path, exist_ok=True)

            df.to_csv(
                feature_store_file_path,
                index=False,
                header=True
            )

            logging.info("Data successfully exported into feature store")

            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, df: pd.DataFrame):

        try:

            train_set, test_set = train_test_split(
                df,
                test_size=self.data_ingestion_config.train_test_split_ratio
            )

            logging.info("Performed train test split on the dataframe")

            dir_path = os.path.dirname(
                self.data_ingestion_config.training_file_path
            )

            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting train and test files")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False,
                header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False,
                header=True
            )

            logging.info("Exported train and test files")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):

        try:

            logging.info("Started data ingestion")

            # Export data from MongoDB
            dataframe = self.export_collection_as_dataframe()

            # Save data into feature store
            dataframe = self.export_data_into_feature_store(
                df=dataframe
            )

            # Split data into train and test
            self.split_data_as_train_test(dataframe)

            # Create data ingestion artifact
            dataingestionartifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info("Completed data ingestion")

            return dataingestionartifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)