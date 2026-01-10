import os
import sys
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from sklearn.preprocessing import OneHotEncoder

from src.exception.exception import CustomerChurnException
from src.logging.logger import logging
from src.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from src.entity.config_entity import DataTransformationConfig
from src.constant.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS, COLUMNS_TO_REMOVE
from src.utils.main_utils import save_object, save_numpy_array_data

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config

    @staticmethod
    def read_data(file_path: str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomerChurnException(e,sys)
    
    def encode_columns(self, train_data: pd.DataFrame, test_data: pd.DataFrame)->pd.DataFrame:
        try:
            for column in train_data.columns:
                if train_data[column].dtype == 'O':
                    ohe = OneHotEncoder(handle_unknown='ignore')
                    train_column_encoded = ohe.fit_transform(train_data[[column]]).toarray()
                    test_column_encoded = ohe.transform(test_data[[column]]).toarray()

                    train_column_encoded = pd.DataFrame(train_column_encoded, columns=ohe.get_feature_names_out([column]))
                    test_column_encoded = pd.DataFrame(test_column_encoded, columns=ohe.get_feature_names_out([column]))

                    train_data.drop(column,axis=1,inplace=True)
                    test_data.drop(column,axis=1,inplace=True)

                    train_data = pd.concat([train_data, train_column_encoded],axis=1)
                    test_data = pd.concat([test_data, test_column_encoded],axis=1)
            
            return train_data, test_data
        except Exception as e:
            raise CustomerChurnException(e,sys)

    def preprocessor_object(self):
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor: Pipeline = Pipeline([("imputer", imputer)])
            return preprocessor
        except Exception as e:
            raise CustomerChurnException(e,sys)
    
    def initiate_data_transformation(self,):
        try:
            logging.info("Initiating Data Transformation")
            logging.info("Reading the Validated Train and Test files")
            train_data = self.read_data(self.data_validation_artifact.valid_train_file_path)
            test_data = self.read_data(self.data_validation_artifact.valid_test_file_path)

            logging.info("Removing Unnecessary Columns")
            train_data = train_data.drop(COLUMNS_TO_REMOVE,axis=1)
            test_data = test_data.drop(COLUMNS_TO_REMOVE,axis=1)

            logging.info("Splitting into Input and Target Data for Preprocessing to prevent Data Leakage")
            input_train_data = train_data.drop(TARGET_COLUMN,axis=1)
            target_train_data = train_data[TARGET_COLUMN]

            input_test_data = test_data.drop(TARGET_COLUMN,axis=1)
            target_test_data = test_data[TARGET_COLUMN]

            logging.info("Encoding Categorical Features using OneHotEncoder")
            input_train_data, input_test_data = self.encode_columns(input_train_data, input_test_data) 

            preprocessor = self.preprocessor_object()

            preprocessor_object = preprocessor.fit(input_train_data)

            logging.info("Imputing Missing Values using KNNImputer")
            transformed_input_train_data = preprocessor_object.transform(input_train_data)
            transformed_input_test_data = preprocessor_object.transform(input_test_data)

            logging.info("Concating Transformed Input and Target Data as Numpy Arrays")
            final_train_data = np.c_[transformed_input_train_data, np.array(target_train_data)]
            final_test_data = np.c_[transformed_input_test_data, np.array(target_test_data)]

            logging.info("Exporting Train and Test Data as Numpy Arrays")
            save_numpy_array_data(final_train_data, self.data_transformation_config.transformed_train_file)
            save_numpy_array_data(final_test_data, self.data_transformation_config.transformed_test_file)

            logging.info("Exporting KNNImputer Object as Pickle file")
            save_object(preprocessor_object, self.data_transformation_config.preprocessor_object)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file,
                preprocessor_object_file_path=self.data_transformation_config.preprocessor_object
            )

            logging.info("Data Transformation Complete")
            return data_transformation_artifact
        except Exception as e:
            raise CustomerChurnException(e,sys)