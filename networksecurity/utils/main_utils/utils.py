import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
#import dill
import pickle

def read_yaml_file(file_path: str) ->dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e


def write_yaml_file(file_path: str,content: object,replace: bool=False)->None:
    try:
        if replace:
            if os.apth.exits(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_numpy_array_data(file_path: str,array: np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e


def save_object(file_path: str,obj: object)->None:
    try:
        logging.info("Entered the save_object method of Mainutils class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

def load_object(file_path: str,)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path,"rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

def load_numpy_array_data(file_path: str)->np.array:
        try:
            with open(file_path,"rb") as file_obj:
                return np.load(file_obj)
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e