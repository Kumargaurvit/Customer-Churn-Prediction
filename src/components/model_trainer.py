import sys

from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier

from src.exception.exception import CustomerChurnException
from src.logging.logger import logging
from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from src.entity.config_entity import ModelTrainerConfig
from src.utils.main_utils import load_numpy_array_data, evaluate_models, load_object, save_object
from src.utils.ml_utils import get_classification_metrics

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact, model_trainer_config: ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise CustomerChurnException(e,sys)
    
    def resample_data(self, X_train, y_train):
        try:
            smote = SMOTE(random_state=42)
            X_train, y_train = smote.fit_resample(X_train, y_train)
            return X_train, y_train
        except Exception as e:
            raise CustomerChurnException(e,sys)
    
    def train_test_split(self):
        try:
            train_data = load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_data = load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)

            X_train, y_train = (
                train_data[:,:-1],
                train_data[:,-1]
            )

            X_test, y_test = (
                test_data[:,:-1],
                test_data[:,-1]
            )

            return X_train, X_test, y_train, y_test
        except Exception as e:
            raise CustomerChurnException(e,sys)

    def train_models(self):
        try:
            models = {
                "Logistic Regression": LogisticRegression(verbose=1, max_iter=10000),
                "Random Forest Classifier" : RandomForestClassifier(
                    class_weight="balanced", n_estimators=200, max_depth=8, n_jobs=-1, verbose=1
                ),
                "Gradient Boosting Classifier" : GradientBoostingClassifier(verbose=1),
                "XGBoost Classifier" : XGBClassifier(),
            }

            logging.info('Train Test Splitting the Train and Test Numpy Arrays')
            X_train, X_test, y_train, y_test = self.train_test_split()

            logging.info('Resampling Data Using SMOTE')
            X_train_smote, y_train_smote = self.resample_data(X_train, y_train)

            logging.info('Training Models using Hyperparameter Tuning')
            model_report, best_models = evaluate_models(
                models, X_train_smote, X_test, y_train_smote, y_test
            )
            
            logging.info('Evaluating Models using Classification Metrics')
            best_model_score = max(sorted(list(model_report.values())))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = best_models[best_model_name]
            logging.info(f'Best Model : {best_model_name}, Accuracy Score : {best_model_score*100:.2f}%')

            y_train_pred = best_model.predict(X_train_smote)
            y_test_pred = best_model.predict(X_test)

            train_metrics = get_classification_metrics(y_train_smote, y_train_pred)
            test_metrics = get_classification_metrics(y_test, y_test_pred)

            preprocessor = load_object(self.data_transformation_artifact.preprocessor_object_file_path)
            ohe = load_object(self.data_transformation_artifact.encoder_object_file_path)

            logging.info('Saving Preprocessing and Model Objects')
            save_object(preprocessor, self.model_trainer_config.preprocessor_file_path)
            save_object(ohe, self.model_trainer_config.encoder_file_path)
            save_object(best_model, self.model_trainer_config.model_file_path)

            return train_metrics, test_metrics
        except Exception as e:
            raise CustomerChurnException(e,sys)
        
    def initiate_model_trainer(self):
        try:
            logging.info('Initiating Model Training')
            train_metrics, test_metrics = self.train_models()

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.model_file_path,
                train_metrics=train_metrics,
                test_metrics=test_metrics
            )

            logging.info('Model Training Completed')
            return model_trainer_artifact
        except Exception as e:
            raise CustomerChurnException(e,sys)