from src.stok_optimizasyonu_ml_project.config.configuration import ConfigurationManager
from src.stok_optimizasyonu_ml_project.components.model_trainer import ModelTrainer
from src.stok_optimizasyonu_ml_project import logger


STAGE_NAME = "Model Trainer Stage"

class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.train()


if __name__ == '__main__':
    try:
        logger.info(f">>>>>>>>> stage: {STAGE_NAME} started <<<<<<<<<<")
        obj = ModelTrainerTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>>>>> stage: {STAGE_NAME} completed <<<<<<<<<<")
    except Exception as e:
        raise e