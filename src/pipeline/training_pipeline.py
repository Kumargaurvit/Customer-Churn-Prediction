import sys

from src.exception.exception import CustomerChurnException
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

class TrainingPipeline:
    def __init__(self, training_pipeline_config = TrainingPipelineConfig):
        try:
            self.training_pipeline_config = training_pipeline_config
        except Exception as e:
            raise CustomerChurnException(e,sys)

    def start_data_ingestion(self):
        try:
            data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise CustomerChurnException(e,sys)

    def start_data_validation(self):
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise CustomerChurnException(e,sys)

    def start_data_transformation(self):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation_artifact = self.start_data_validation()
            data_transformation = DataTransformation(
                data_validation_artifact=data_validation_artifact,data_transformation_config=data_transformation_config
            )
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise CustomerChurnException(e,sys)

    def start_model_trainer(self):
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation_artifact = self.start_data_transformation()
            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,model_trainer_config=model_trainer_config
            )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise CustomerChurnException(e,sys)
        
    def initiate_training_pipeline(self):
        try:
            model_trainer_artifact = self.start_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise CustomerChurnException(e,sys)