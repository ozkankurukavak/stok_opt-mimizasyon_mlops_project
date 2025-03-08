from src.stok_optimizasyonu_ml_project.config.configuration import ConfigurationManager
from src.stok_optimizasyonu_ml_project.components.data_ingestion import DataIngestion
from src.stok_optimizasyonu_ml_project import logger


STAGE_NAME1 = 'data_ingestion'
class DataIngestionTrainingPipeline:
    def __iniit__(self):
        pass


    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()

if __name__ == '__main__':
    try:
        # Aşamanın başladığını kaydet
        logger.info(f">>>>>>>>>> stage {STAGE_NAME1} started <<<<<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        # Aşamanın tamamlandığını kaydet
        logger.info(f">>>>>>>>>> stage {STAGE_NAME1} completed <<<<<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e