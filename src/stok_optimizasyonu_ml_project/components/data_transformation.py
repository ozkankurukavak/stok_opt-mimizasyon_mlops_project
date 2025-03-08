import os
from src.stok_optimizasyonu_ml_project import logger
from sklearn.model_selection import train_test_split
import pandas as pd
from src.stok_optimizasyonu_ml_project.utils.common import get_size
import re
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.stok_optimizasyonu_ml_project import logger


import pandas as pd
import re
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn.impute import SimpleImputer

class DataTransformation:
    def __init__(self, config):
        self.config = config

    def transform(self):
        try:
            # Adım 1: Veriyi Yükle
            df = pd.read_csv(self.config.data_path)  # Veriyi `data_path`'ten yükle

            # Adım 2: Tarih işlemleri - Yıl, Ay, Gün, Hafta Günü ekle
            df['SalesDate'] = pd.to_datetime(df['SalesDate'])
            df['Year'] = df['SalesDate'].dt.year
            df['Month'] = df['SalesDate'].dt.month
            df['Day'] = df['SalesDate'].dt.day
            df['Weekday'] = df['SalesDate'].dt.weekday
            df.drop('SalesDate', axis=1, inplace=True)

            # Adım 3: Ordinal Encoding - Size_sales ve Size_purchase
            size_sales_order = sorted(df['Size_sales'].unique())  # Benzersiz değerleri sıralıyoruz
            size_purchase_order = sorted(df['Size_purchase'].unique())  # Benzersiz değerleri sıralıyoruz

            encoder_sales = OrdinalEncoder(categories=[size_sales_order])
            df['Size_sales_encoded'] = encoder_sales.fit_transform(df[['Size_sales']])

            encoder_purchase = OrdinalEncoder(categories=[size_purchase_order])
            df['Size_purchase_encoded'] = encoder_purchase.fit_transform(df[['Size_purchase']])

            # Adım 4: Label Encoding - Nominal veriler için encoding
            nominal_columns = ['InventoryId', 'Description_sales', 'VendorName_sales', 'Description_purchase', 'VendorName_purchase']
            label_encoder = LabelEncoder()
            for col in nominal_columns:
                df[col] = label_encoder.fit_transform(df[col])

            # Adım 5: Boyut işlemleri - Size_sales ve Size_purchase dönüşümleri
            def convert_size(size):
                try:
                    if "Pk" in size:
                        match = re.search(r"(\d+)(mL|L).*?(\d+)\s*Pk", size)
                        if match:
                            amount = int(match.group(1))  # mL veya L değeri
                            unit = match.group(2)        # Birim (mL veya L)
                            pack = int(match.group(3))   # Paket sayısı
                            if unit == "L":
                                amount *= 1000  # L → mL çevir
                            return amount * pack  # Toplam hacim

                    elif "mL" in size:
                        match = re.search(r"(\d+)(mL)", size)
                        if match:
                            return int(match.group(1))  # Sadece mL değeri al

                    elif "L" in size:
                        match = re.search(r"(\d+\.\d+|\d+)(L)", size)
                        if match:
                            return float(match.group(1)) * 1000  # L → mL çevir

                    elif "Oz" in size:
                        match = re.search(r"(\d+\.\d+|\d+)", size)
                        if match:
                            return float(match.group(1)) * 29.5735  # Oz → mL çevir

                    else:
                        return None  # Hatalı girişleri atla
                except Exception as e:
                    return None  # Hatalı durumlarda None döndür

            df['Size_sales'] = df['Size_sales'].apply(convert_size)
            df['Size_purchase'] = df['Size_purchase'].apply(convert_size)

            # Median ile eksik değerleri doldur
            median_value = df['Size_sales'].median()
            df['Size_sales'] = df['Size_sales'].fillna(median_value)

            # Veriyi Pipeline üzerinden işle
            self.apply_pipeline(df)

            # Adım 6: Veriyi Kaydet
            self.save_data(df)  # İşlenmiş veriyi kaydet

            return df

        except Exception as e:
            # Hata durumunda hata mesajını fırlat
            raise e

    def apply_pipeline(self, df):
        # Öznitelik sütunlarını tanımla
        size_columns = ['Size_sales', 'Size_purchase']
        nominal_columns = ['InventoryId', 'Description_sales', 'VendorName_sales', 'Description_purchase', 'VendorName_purchase']

        # Pipeline setup
        # Kategoriler her sütun için ayrı ayrı tanımlanmalı
        pipeline = Pipeline(steps=[
            ('impute_size_sales', SimpleImputer(strategy='median')),  # Eksik verileri median ile doldur
            ('ordinal_encoder_sales', OrdinalEncoder(categories=[sorted(df['Size_sales'].unique())])),  # Size_sales için Ordinal encoding
            ('ordinal_encoder_purchase', OrdinalEncoder(categories=[sorted(df['Size_purchase'].unique())]))  # Size_purchase için Ordinal encoding
        ])

        # Veriye pipeline uygula
        df['Size_sales'] = pipeline.named_steps['ordinal_encoder_sales'].fit_transform(df[['Size_sales']])
        df['Size_purchase'] = pipeline.named_steps['ordinal_encoder_purchase'].fit_transform(df[['Size_purchase']])

        # Nominal sütunlar için LabelEncoder'ı uygulayalım
        for col in nominal_columns:
            df[col] = LabelEncoder().fit_transform(df[col])

    def save_data(self, df):
        """
        İşlenmiş veriyi config.yaml'daki belirtilen yola kaydeder.
        """
        output_path = self.config.transformed_data_path  # config.yaml'dan doğru yolu al
        df.to_csv(output_path, index=False)
        print(f"Veri başarıyla kaydedildi: {output_path}")