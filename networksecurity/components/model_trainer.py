import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifacts_entity import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.main_utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import (
    save_object,
    load_object,
    load_numpy_array_data,
)
import mlflow
from sklearn.model_selection import GridSearchCV
from networksecurity.utils.main_utils.ml_utils.metric.classification_metric import get_classification_score
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import(
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)




class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def track_mlflow(self,best_model,classificationmetric):
        with mlflow.start_run():
            f1_score=classificationmetric.f1_score
            precision_score=classificationmetric.precision_score
            recall_score=classificationmetric.recall_score

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision",precision_score)
            mlflow.log_metric("recall_score",recall_score)

            mlflow.sklearn.log_model(best_model,"model")



    def train_model(self,x_train,y_train,x_test,y_test):
        models={
            "Random Forest":RandomForestClassifier(verbose=1),
            "Decision Tree":DecisionTreeClassifier(),
            "Gradient Boosting":GradientBoostingClassifier(verbose=1),
            "Logistic Regression":LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier(),
        }

        params={
            "Decision Tree":{
                'criterion':['gini','entropy','log_loss'],
            },
            "Random Forest":{
                'n_estimators':[8,16,32,64,128,256]
            },
            "Gradient Boosting":{
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.8,0.05,0.9],
                'n_estimators':[8,16,32,64,128,256]
            },
            "Logistic Regression":{ "C": [0.1, 1.0, 10.0]},
            "AdaBoost":{
                'learning_rate':[.1,.01,0.5,.001],
                'n_estimators':[8,16,32,64,128,256]
            }
        }

        model_report=self.evaluate_models(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,param=params,models=models)
        
        best_model_name = max(model_report, key=model_report.get)
        best_model = models[best_model_name]

        y_train_pred=best_model.predict(x_train)

        classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)

        ##Track the experiments with mlflow
        
        mlflow.sklearn.log_model(
        best_model,
        "model",
        skops_trusted_types=["sklearn.tree._tree.Tree"]
)

        y_test_pred = best_model.predict(x_test)
        classification_test_metric = get_classification_score(
        y_true=y_test, y_pred=y_test_pred
        )
        preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(
        self.model_trainer_config.trained_model_file_path,
        obj=network_model
)

        ##ModelTrainer Artifact

        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_artifact=classification_test_metric)

        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact

    
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            print("Train array shape:", train_arr.shape)
            print("Test array shape:", test_arr.shape)
            print("Train array sample:", train_arr[:2])

            x_train = train_arr[:, :-1]
            y_train = train_arr[:, -1]
            x_test = test_arr[:, :-1]
            y_test = test_arr[:, -1]

            return self.train_model(x_train, y_train, x_test, y_test)

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def evaluate_models(self,x_train,y_train,x_test,y_test,models,param):
        try:
            report={}
            for i in range(len(list(models))):
                model=list(models.values())[i]
                para=param[list(models.keys())[i]]

                gs=GridSearchCV(model,para,cv=3)
                gs.fit(x_train,y_train)

                model.set_params(**gs.best_params_)
                model.fit(x_train,y_train)

                y_train_pred=model.predict(x_train)
                y_test_pred=model.predict(x_test)

                train_model_score = f1_score(
                y_train,
                y_train_pred,
                average="weighted",
                zero_division=0
)

                test_model_score = f1_score(
                y_test,
                y_test_pred,
                average="weighted",
                zero_division=0
)

                report[list(models.keys())[i]] = test_model_score

                

            return report
        except Exception as e:
            raise NetworkSecurityException(e,sys)
