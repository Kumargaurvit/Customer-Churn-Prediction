import sys

from src.exception.exception import CustomerChurnException
from src.pipeline.training_pipeline import TrainingPipeline
from src.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        training_pipeline = TrainingPipeline(training_pipeline_config=training_pipeline_config)
        training_pipeline.initiate_training_pipeline()
    except Exception as e:
            raise CustomerChurnException(e,sys)