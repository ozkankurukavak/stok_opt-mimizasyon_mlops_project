import os
import urllib.request as request
import zipfile
from src.stok_optimizasyonu_ml_project import logger
from src.stok_optimizasyonu_ml_project.utils.common import get_size
from pathlib import Path
from src.stok_optimizasyonu_ml_project.entitiy.config_entitiy import DataIngestionConfig


class DataIngestion:
    def __init__(self,config: DataIngestionConfig): # config parametresi DataIngestionConfig icerisnde olusturulmus degiskenlerini ve tiplerini almasi saglaniyor
        self.config = config # config degiskenine deger olarak DataIngestion sinifindan nesne olusturken config parametresinin yerine ne deger ataniyorsa aynisi config degiskenine atanmasi saglaniyor


    
    def download_file(self):
        if not os.path.exists(self.config.local_data_file): # data.zip isimli bir dosya yoksa True Donecektir
            filename, headers = request.urlretrieve(
                url = self.config.source_URL, # url parametre dosyanin hangi siteden indirilmesi gerektigini alir
                filename = self.config.local_data_file # dosyayi hangi isimle locale indirmen gerektigini yazar
            )
            logger.info(f"{filename} download! with following info: \n{headers}")
        else: # eger onceden boyle bir dosya varsa
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")  #data.zip dosyasinin kb olarak ne kadar buyuk oldugunu loglar


    
    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir # unzip_path degiskenine artifacts/data_ingestion bu degeri atiyoruz
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref: # zip_ref adini verdigimiz bir degiskenle data.zipin icerini acip okuyoruz
            zip_ref.extractall(unzip_path) # extractall metoduyla dosyami zipten cikarip artifacts/data_ingestion bu klasor icerisine atiyorum

    