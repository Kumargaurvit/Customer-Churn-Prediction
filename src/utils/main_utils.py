from src.exception.exception import CustomerChurnException

import os
import sys
import numpy as np
import yaml
import pickle

def read_yaml_file(file_path: str):
    try:
        with open(file_path,"rb") as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise CustomerChurnException(e,sys)

def write_yaml_file(file_path: str, content: object, replace: bool = False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise CustomerChurnException(e,sys)

def save_object(object, file_path: str):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path,"wb") as file:
            pickle.dump(object, file)
    except Exception as e:
        raise CustomerChurnException(e,sys)
    
def save_numpy_array_data(array: np.array, file_path: str):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path,"wb") as file:
            np.save(file, array)
    except Exception as e:
        raise CustomerChurnException(e,sys)