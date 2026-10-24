
import sys
import os
import certifi

from dotenv import load_dotenv
load_dotenv()

import pymongo
from pymongo import MongoClient

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.ml_utils.model.estimator import NetworkModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.constants.training_pipeline import (
    DATA_INGESTION_DATABASE_NAME,
    DATA_INGESTION_COLLECTION_NAME
)

mongo_db_url = os.getenv("MONGO_DB_URL")

if not mongo_db_url:
    raise ValueError("MONGO_DB_URL is not set in the .env file")

client = MongoClient(mongo_db_url, tlsCAFile=certifi.where())

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="./templates")


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")

    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.post("/predict")
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        preprocessor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model=NetworkModel(preprocessor=preprocessor,model=final_model)
        print(df.iloc[0])
        y_pred=network_model.predict(df)
        print(y_pred)
        df['predicted_column']=y_pred
        print(df['predicted_column'])
        df.to_csv("prediction_output/output.csv")
        table_html=df.to_html(classes='tabletable-striped')
        return templates.TemplateResponse(
        request=request,
        name="table.html",
        context={"table": table_html}
        )
    except Exception as e:
        raise NetworkSecurityException(e,sys)

if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)
