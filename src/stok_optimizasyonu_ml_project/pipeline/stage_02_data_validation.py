from src.stok_optimizasyonu_ml_project.config.configuration import ConfigurationManager
from src.stok_optimizasyonu_ml_project.components.data_validation import DataValidation
from src.stok_optimizasyonu_ml_project import logger
import pandas as pd



STAGE_NAME = 'Data validation stage'

class DataValidationTrainingPipline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        
        # Veri doğrulamasını yapıyoruz
        validation_status = data_validation.validate_all_columns()
        
        if not validation_status:
            # Validation başarısızsa, log kaydı ekleyebiliriz
            with open(data_validation.config.STATUS_FILE, 'a') as f:  # Burada 'self' yerine 'data_validation.config' kullanıyoruz
                f.write(f"Data validation failed at {pd.to_datetime('now')}\n")


if __name__ == 'main':
    try:
        logger.info(f">>>>>>>>>> stage: {STAGE_NAME}  started <<<<<<<<<<")
        obj = DataValidationTrainingPipline()
        obj.main()
        logger.info(f">>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e