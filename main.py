from src.stok_optimizasyonu_ml_project import logger
from src.stok_optimizasyonu_ml_project.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from src.stok_optimizasyonu_ml_project.pipeline.stage_02_data_validation import DataValidationTrainingPipline


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