import os
import sys
import numpy as np
import yaml
import pickle

from sklearn.metrics import f1_score

from src.exception.exception import CustomerChurnException

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

def load_object(file_path: str):
    try:
        with open(file_path, "rb") as file:
            return pickle.load(file)
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

def load_numpy_array_data(file_path: str)->np.array:
    try:
        with open(file_path, "rb") as file:
            return np.load(file)
    except Exception as e:
        raise CustomerChurnException(e,sys)
    
def evaluate_models(models, X_train, X_test, y_train, y_test):
    try:
        report = {}
        best_models = {}
        for i in range(len(models)):
            model_name = list(models.keys())[i]
            model = list(models.values())[i]

            model.fit(X_train, y_train)
        
            test_y_pred = model.predict(X_test)
            
            test_f1 = f1_score(y_test, test_y_pred)

            report[model_name] = test_f1
            best_models[model_name] = model

        return report, best_models
    except Exception as e:
        raise CustomerChurnException(e,sys)