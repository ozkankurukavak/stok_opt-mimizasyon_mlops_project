import os
from src.stok_optimizasyonu_ml_project import logger
from src.stok_optimizasyonu_ml_project.entitiy.config_entitiy import DataValidationConfig
import pandas as pd
from scipy.stats import zscore

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config
        
    def validate_all_columns(self) -> bool:
        try:
            validation_status = True  # Başlangıçta doğrulama başarılı (True)
            
            # Veriyi okuyoruz
            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = list(data.columns)  # Kolon isimlerini alıyoruz
            all_schema = self.config.all_schema.keys()  # Şemadaki kolon isimleri
            
            # Kolonları kontrol et
            for col in all_cols:
                if col not in all_schema:
                    validation_status = False  # Kolon eksikse False dönecek
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}, Error: Missing Column - {col}")
                    return validation_status  # Eğer bir kolon eksikse işlemi sonlandırıyoruz

            # Kolon sırasını kontrol et (Eğer gereksinim varsa)
            expected_columns = list(self.config.all_schema.keys())
            if all_cols != expected_columns:
                validation_status = False
                with open(self.config.STATUS_FILE, 'w') as f:
                    f.write(f"Validation status: {validation_status}, Error: Column Order mismatch.")

            # Eksik veri kontrolü
            missing_data = data.isnull().sum()  # Her kolondaki eksik veri sayısını alıyoruz
            if missing_data.any():  # Eğer eksik veri varsa
                validation_status = False
                with open(self.config.STATUS_FILE, 'w') as f:
                    f.write(f"Validation status: {validation_status}, Missing Data: {missing_data}")
                return validation_status  # Eksik veri bulunduğunda işlemi sonlandırıyoruz
            
            # Z-Score ile aykırı değer analizi (Status'u etkilemeden raporlama)
            outliers_dict = self.zscore_analysis_multi(data, columns=all_cols, threshold=3)  # Z-score ile aykırı değer analizi
            with open(self.config.STATUS_FILE, 'a') as f:
                f.write(f"Outliers detected: {outliers_dict}\n")  # Aykırı değerleri raporluyoruz

            return validation_status  # Doğrulama başarılı ise True dönecek
        
        except Exception as e:
            validation_status = False
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}, Error: {str(e)}")
            return validation_status

    def zscore_analysis_multi(self, df: pd.DataFrame, columns: list, threshold: float = 3):
        outliers_dict = {}
        
        # Z-score analizi için yalnızca sayısal kolonları alıyoruz
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        
        # Z-score hesaplamak için sadece sayısal verilere odaklanıyoruz
        for column in numeric_columns:
            try:
                df[f'{column}_zscore'] = zscore(df[column])  # Z-score hesaplama
                outliers = df[df[f'{column}_zscore'].abs() > threshold]  # Z-Score threshold'unu geçenler
                outliers_dict[column] = outliers
            except Exception as e:
                # Eğer hata oluşursa (örneğin bir sütunda yalnızca string değerler varsa), bu hatayı kaydet
                outliers_dict[column] = f"Error in Z-score calculation: {str(e)}"
        
        return outliers_dict