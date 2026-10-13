import os
import sys
import numpy as np
import pandas as pd


TARGET_COLUMN="Result"
PIPELINE_NAME:str="networksecurity"
ARTIFACT_DIR:str="artifact"
FILE_NAME:str="phisingData.csv"

TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"

SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")

DATA_INGESTION_COLLECTION_NAME:str="NetworkData"
DATA_INGESTION_DIR_NAME:str="sanjanaaai"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_DATABASE_NAME:str="KNAacademy"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION:float=0.2
DATA_INGESTION_INGESTED_DIR:str="ingested"

DATA_VALIDATION_DIR_NAME: str="data_validation"
DATA_VALIDATION_VALID_DIR: str="validated"
DATA_VALIDATION_INVALID_DIR: str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str="report.yaml"

"""
Data transformation related constant start with Data_transformation var name
"""

DATA_TRANSFORMATION_DIR_NAME: str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str="transformed"
DATA_TRANSFORMED_TRANSFORMED_ODJECT_DIR: str="transformed_object"
PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"

##knn imputed class -to replace nan values
DATA_TRANSFORMATION_IMPUTED_PARAMS: dict={
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights": "uniform",
}