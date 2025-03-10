from src.stok_optimizasyonu_ml_project import logger
from src.stok_optimizasyonu_ml_project.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from src.stok_optimizasyonu_ml_project.pipeline.stage_02_data_validation import DataValidationTrainingPipline
from src.stok_optimizasyonu_ml_project.pipeline.stage_03_data_transformation import DataTransformationTrainingPipline
from src.stok_optimizasyonu_ml_project.pipeline.stage_04_model_trainer import ModelTrainerTrainingPipeline

STAGE_NAME = 'Data Ingestion stage'

try:
    # Aşamanın başladığını kaydet
    logger.info(f">>>>>>>>>> stage {STAGE_NAME} started <<<<<<<<<")
    obj = DataIngestionTrainingPipeline()
    obj.main() # pipeline/data_ingestion.py içerisinde DataIngestionTrainingPipeline class içerisindeki main
    # Aşamanın tamamlandığını kaydet
    logger.info(f">>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<")
except Exception as e:
    logger.exception(e)
    raise e




STAGE_NAME = 'Data Validation stage'

try:
    # Aşamanın başladığını kaydet
    logger.info(f">>>>>>>>>> stage {STAGE_NAME} started <<<<<<<<<")
    obj = DataValidationTrainingPipline()
    obj.main() # pipeline/data_ingestion.py içerisinde DataValidationTrainingPipeline class içerisindeki main
    # Aşamanın tamamlandığını kaydet
    logger.info(f">>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<")
except Exception as e:
    logger.exception(e)
    raise e




STAGE_NAME = 'Data Transformation stage'

try:
    # Aşamanın başladığını kaydet
    logger.info(f">>>>>>>>>> stage {STAGE_NAME} started <<<<<<<<<")
    obj = DataTransformationTrainingPipline()
    obj.main() # pipeline/data_ingestion.py içerisinde DataValidationTrainingPipeline class içerisindeki main
    # Aşamanın tamamlandığını kaydet
    logger.info(f">>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<")
except Exception as e:
    logger.exception(e)
    raise e




STAGE_NAME = 'Model Trainer Stage'

try:
        logger.info(f">>>>>>>>> stage: {STAGE_NAME} started <<<<<<<<<<")
        obj = ModelTrainerTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>>>>> stage: {STAGE_NAME} completed <<<<<<<<<<")
except Exception as e:
        logger.exception(e)
        raise e