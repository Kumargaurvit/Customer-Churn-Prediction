from src.exception.exception import CustomerChurnException
from src.logging.logger import logging

from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from src.utils.main_utils import read_yaml_file, write_yaml_file
from src.constant.training import SCHEMA_FILE_PATH

import os
import sys
import pandas as pd
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.data_schema = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomerChurnException(e,sys)
    
    def read_data(self, file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomerChurnException(e,sys)
        
    def validate_number_of_columns(self, dataframe: pd.DataFrame)->bool:
        try:
            number_of_columns = len(self.data_schema["columns"])
            logging.info(f"Required Number of Columns : {number_of_columns}")
            logging.info(f"Number of DataFrame Columns : {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise CustomerChurnException(e,sys)
    
    def detect_data_drift(self, base_df, current_df, threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column : {
                    "pvalue" :  float(is_same_dist.pvalue),
                    "drift_status" : is_found
                }})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            # Creating and Saving Data Drift Report
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)

            write_yaml_file(drift_report_file_path, report)

            return status
        except Exception as e:
            raise CustomerChurnException(e,sys)
    
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            logging.info("Initiating Data Validation")
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Reading Train and Test Data
            train_data = self.read_data(train_file_path)
            test_data = self.read_data(test_file_path)

            logging.info("Validating Number of Columns")
            status = self.validate_number_of_columns(train_data)
            if not status:
                error_message = f"Train Dataframe does not contain all columns\n"
                logging.info(error_message)
            status = self.validate_number_of_columns(test_data)
            if not status:
                error_message = f"Test Dataframe does not contain all columns\n"
                logging.info(error_message)
            logging.info(f"Column Validation Status : {status}")

            logging.info("Checking if Numerical Columns Exist")
            train_numerical_columns = train_data.select_dtypes(include=['number'])
            if train_numerical_columns.shape[1] == 0:
                error_message = f"No Numerical Columns Found"
                logging.info(error_message)
            
            test_numerical_columns = test_data.select_dtypes(include=['number'])
            if test_numerical_columns.shape[1] == 0:
                error_message = f"No Numerical Columns Found"
                logging.info(error_message)

            logging.info("Checking for Data Drift")
            status = self.detect_data_drift(base_df=train_data,current_df=test_data)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Data Drift Status : {status}")

            logging.info("Exporting Valid Train and Test Data")
            train_data.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True
            )
            test_data.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info("Data Validation Complete")
            return data_validation_artifact
        except Exception as e:
            raise CustomerChurnException(e,sys)