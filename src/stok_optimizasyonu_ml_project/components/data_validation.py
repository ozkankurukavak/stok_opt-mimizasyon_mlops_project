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
            
            # Aykırı Değer Analizi (Outlier Analysis)
            outlier_data = self.outlier_analysis(data, threshold=1.5)  # Aykırı değer analizi
            if outlier_data:
                validation_status = False
                with open(self.config.STATUS_FILE, 'w') as f:
                    f.write(f"Validation status: {validation_status}, Outliers found: {outlier_data}")

            # Z-Score Aykırı Değer Analizi
            outliers_dict = self.zscore_analysis_multi(data, columns=all_cols, threshold=3)  # Z-score ile aykırı değer analizi
            if outliers_dict:
                validation_status = False
                with open(self.config.STATUS_FILE, 'w') as f:
                    f.write(f"Validation status: {validation_status}, Z-score outliers: {outliers_dict}")

            # Validation durumu yazıyoruz
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")
            
            return validation_status  # Sonuç döndürülüyor
        except Exception as e:
            raise e  # Hata durumunda istisna fırlatılır

    # Aykırı değer tespiti (IQR - Interquartile Range) ile
    def outlier_analysis(self, df, threshold=1.5):
        outlier_data = {}
        numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()  # Sayısal kolonları seçiyoruz

        for column in numerical_columns:
            Q1 = df[column].quantile(0.25)  # 1st quartile (Q1)
            Q3 = df[column].quantile(0.75)  # 3rd quartile (Q3)
            IQR = Q3 - Q1  # Interquartile Range (IQR)

            lower_limit = Q1 - threshold * IQR  # Alt sınır
            upper_limit = Q3 + threshold * IQR  # Üst sınır

            # Aykırı değerleri tespit ediyoruz
            outlier_mask = (df[column] < lower_limit) | (df[column] > upper_limit)
            outlier_data[column] = {
                "lower_limit": lower_limit,
                "upper_limit": upper_limit,
                "outlier_count": outlier_mask.sum(),  # Aykırı değerlerin sayısı
                "percentage": round((outlier_mask.sum() / len(df)) * 100, 2)  # Yüzde oranı
            }

        return outlier_data  # Aykırı değerleri döndürüyoruz

    # Z-score ile aykırı değer analizi (Sayısal kolonlar için)
    def zscore_analysis_multi(self, df, columns, threshold=3):
        outliers_dict = {}

        for column in columns:
            df[f'{column}_zscore'] = zscore(df[column])  # Z-score hesaplama

            # Z-score değeri belirli bir eşik değerini aşarsa aykırı değer olarak işaretliyoruz
            outlier_mask = (df[f'{column}_zscore'] > threshold) | (df[f'{column}_zscore'] < -threshold)

            outliers_dict[column] = df[outlier_mask]  # Aykırı değerleri kaydediyoruz

        return outliers_dict  # Aykırı değerlerin bulunduğu dictionary döndürülüyor