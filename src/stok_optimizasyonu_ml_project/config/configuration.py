from src.stok_optimizasyonu_ml_project.constants import *
from src.stok_optimizasyonu_ml_project.utils.common import read_yaml,create_directories
from src.stok_optimizasyonu_ml_project.entitiy.config_entitiy import (DataIngestionConfig,DataValidationConfig)

class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH, schema_filepath = SCHEMA_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        print("Yüklenen config:", self.config)  # Debug için eklendi
        
        create_directories([self.config.artifacts_root])


    
    def get_data_ingestion_config(self) -> DataIngestionConfig: # Yukarida DataIngestionConfig sinifi icerisinde tanimlamis oldugum degiskenleri return edecektir
        config = self.config.data_ingestion # root_dir, local_data_file, source_URL, unzip_dir keylerine erisim sagliyorum

        create_directories([config.root_dir]) # artifacts/data_ingestion isimli bir klasor olustuyorum

        data_ingestion_config = DataIngestionConfig( # Ust hucrede tanimlamis oldugum sinifin nesnesini yaratiyorum
            root_dir=config.root_dir, #artifacts/data_ingestion
            source_URL=config.source_URL, #https://www.kaggle.com/api/v1/datasets/download/bhavikjikadara/student-study-performance
            local_data_file=config.local_data_file, # artifacts/data_ingestion/data.zip
            unzip_dir=config.unzip_dir, # artifacts/data_ingestion
        )

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir = config.root_dir,
            STATUS_FILE= config.STATUS_FILE,
            unzip_data_dir = config.unzip_data_dir,
            all_schema = schema
        )

        return data_validation_config