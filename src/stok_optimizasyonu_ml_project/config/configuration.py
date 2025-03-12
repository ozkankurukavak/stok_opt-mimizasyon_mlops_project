from src.stok_optimizasyonu_ml_project.constants import *
from src.stok_optimizasyonu_ml_project.utils.common import read_yaml,create_directories
from src.stok_optimizasyonu_ml_project.entitiy.config_entitiy import (DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig)

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
    
    
    
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation

        # Root directory için Path nesnesi oluşturuluyor
        root_dir = Path(config.root_dir)
        data_path = Path(config.data_path)
        transformed_data_path = Path(config.transformed_data_path)  # Yeni eklenen kısım

        create_directories([root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=root_dir,
            data_path=data_path,
            transformed_data_path=transformed_data_path  # Yeni eklenen kısım
    )

        return data_transformation_config
    


    def get_model_trainer_config(self) -> ModelTrainerConfig:
        # Config, params ve schema'ya erişim sağlıyoruz
        config = self.config.model_trainer
        params = self.params.xgboost  # params.yaml'dan XGBoost parametreleri
        schema = self.schema.TARGET_COLUMN  # target_column bilgisi schema.yaml'dan

        # Klasörlerin oluşturulması
        create_directories([config.root_dir])

        # ModelTrainerConfig'i döndürüyoruz
        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            train_data_path=config.train_data_path,
            test_data_path=config.test_data_path,
            model_name=config.model_name,
            target_column=schema.name,  # Target sütunu
            xgboost_params=params,  # XGBoost parametrelerini geçiyoruz
        )
        
        return model_trainer_config