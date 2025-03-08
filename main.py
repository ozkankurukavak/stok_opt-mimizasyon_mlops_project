from src.stok_optimizasyonu_ml_project import logger
from src.stok_optimizasyonu_ml_project.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline


STAGE_NAME1 = 'Data Ingestion stage'

try:
    # Aşamanın başladığını kaydet
    logger.info(f">>>>>>>>>> stage {STAGE_NAME1} started <<<<<<<<<")
    obj = DataIngestionTrainingPipeline()
    obj.main() # pipeline/data_ingestion.py içerisinde DataIngestionTrainingPipeline class içerisindeki main
    # Aşamanın tamamlandığını kaydet
    logger.info(f">>>>>>>>>> stage {STAGE_NAME1} completed <<<<<<<<<<")
except Exception as e:
    logger.exception(e)
    raise e