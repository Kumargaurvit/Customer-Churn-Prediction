import sys
import pandas as pd

from src.exception.exception import CustomerChurnException
from src.entity.artifact_entity import ClassificationMetric
from sklearn.metrics import f1_score, precision_score, recall_score

from src.utils.main_utils import load_object
from src.entity.config_entity import ModelTrainerConfig, TrainingPipelineConfig

def get_classification_metrics(y_true, y_pred)->ClassificationMetric:
    try:
        f1 = f1_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)

        classification_metric = ClassificationMetric(
            f1=f1,
            precision=precision,
            recall=recall
        )

        return classification_metric
    except Exception as e:
        raise CustomerChurnException(e,sys)

def preprocess(data: pd.DataFrame)->float:
    try:
        training_pipeline_config = TrainingPipelineConfig()
        model_trainer_config = ModelTrainerConfig(training_pipeline_config)

        ohe = load_object(model_trainer_config.encoder_file_path)
        knn = load_object(model_trainer_config.preprocessor_file_path)
        model = load_object(model_trainer_config.model_file_path)

        cat_cols = list(ohe.feature_names_in_)

        column_encoded = ohe.transform(data[cat_cols]).toarray()

        column_encoded = pd.DataFrame(column_encoded, columns=ohe.get_feature_names_out(), index=data.index)

        data.drop(cat_cols, axis=1, inplace=True)

        data = pd.concat([data,column_encoded],axis=1)
        
        data = knn.transform(data)

        return data, model
    except Exception as e:
        raise CustomerChurnException(e,sys)