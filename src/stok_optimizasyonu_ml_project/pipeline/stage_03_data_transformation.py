from src.stok_optimizasyonu_ml_project.config.configuration import ConfigurationManager
from src.stok_optimizasyonu_ml_project.components.data_transformation import DataTransformation 
from src.stok_optimizasyonu_ml_project import logger
import pandas as pd
from pathlib import Path


STAGE_NAME = 'Data transformation stage'

class DataTransformationTrainingPipline:
    def __init__(self):
        pass

    def main(self):
        try:
            with open(Path("artifacts/data_validation/status.txt"),"r") as f:
                status = f.read().split(" ")[-1]

                if status == 'True':
                    config = ConfigurationManager()
                    data_transformation_config = config.get_data_transformation_config()
                    data_transformation = DataTransformation(config=data_transformation_config)
                    data_transformation.train_test_spliting()
                else:
                    raise Exception("You data schema is not valid")
        except Exception as e:
            print(e)


if __name__ =='main':
    try:
        logger.info(f">>>>>>>>> stage: {STAGE_NAME} started <<<<<<<<<<")
        obj = DataTransformationTrainingPipline()
        obj.main()
        logger.info(f">>>>>>>>>> stage: {STAGE_NAME} completed <<<<<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e