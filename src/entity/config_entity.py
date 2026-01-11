import os
from datetime import datetime

from src.constant import training

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%d-%m-%Y-%H-%M-%S")
        self.pipeline_name = training.PIPELINE_NAME
        self.artifact_name = training.ARTIFACT_DIR
        self.final_models = training.FINAL_MODEL_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.timestamp: str = timestamp
        self.model_dir: str = os.path.join('final_models')

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_path: str = os.path.join(
            self.data_ingestion_dir, training.DATA_INGESTION_FEATURE_STORE_DIR, training.FILE_NAME
        )
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir, training.DATA_INGESTION_INGESTED_DIR, training.TRAIN_FILE_NAME
        )
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir, training.DATA_INGESTION_INGESTED_DIR, training.TEST_FILE_NAME
        )

        self.train_test_split_ratio: float = training.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.database_name: str = training.DATABASE_NAME
        self.collection_name: str = training.COLLECTION_NAME

class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training.DATA_VALIDATION_DIR_NAME
        )
        self.valid_data_dir: str = os.path.join(
            self.data_validation_dir, training.DATA_VALIDATION_VALID_DIR
        )
        self.invalid_data_dir: str = os.path.join(
            self.data_validation_dir, training.DATA_VALIDATION_INVALID_DIR
        )
        self.valid_train_file_path: str = os.path.join(
            self.valid_data_dir, training.TRAIN_FILE_NAME
        )
        self.valid_test_file_path: str = os.path.join(
            self.valid_data_dir, training.TEST_FILE_NAME
        )
        self.invalid_train_file_path: str = os.path.join(
            self.invalid_data_dir, training.TRAIN_FILE_NAME
        )
        self.invalid_test_file_path: str = os.path.join(
            self.invalid_data_dir, training.TEST_FILE_NAME
        )
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir, training.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )

class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training.DATA_TRANSFORMATION_DIR_NAME
        )
        self.transformed_train_file: str = os.path.join(
            self.data_transformation_dir, training.DATA_TRANSFORMATION_TRANSFORMED_DIR_NAME,
            training.TRAIN_FILE_NAME
        )
        self.transformed_test_file: str = os.path.join(
            self.data_transformation_dir, training.DATA_TRANSFORMATION_TRANSFORMED_DIR_NAME,
            training.TEST_FILE_NAME
        )
        self.preprocessor_object: str = os.path.join(
            self.data_transformation_dir, training.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR_NAME,
            training.PREPROCESSOR_OBJECT_NAME
        )
        self.encoder_object: str = os.path.join(
            self.data_transformation_dir, training.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR_NAME,
            training.ENCODER_OBJECT_NAME
        )

class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_file_path: str = os.path.join(
            training_pipeline_config.final_models, training.MODEL_FILE_NAME
        )
        self.preprocessor_file_path: str = os.path.join(
            training_pipeline_config.final_models, training.PREPROCESSOR_OBJECT_NAME
        )
        self.encoder_file_path: str = os.path.join(
            training_pipeline_config.final_models, training.ENCODER_OBJECT_NAME
        )
        self.scaler_file_path: str = os.path.join(
            training_pipeline_config.final_models, training.SCALER_OBJECT_NAME
        )