import os
from box.exceptions import BoxValueError
import yaml
import json
import joblib
from ensure import ensure_annotations
from box import Box
from pathlib import Path
from typing import Any
import base64
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> Box:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)  # YAML dosyasını okur.
            return Box(content)  # YAML içeriğini Box formatında döndürür.
    except BoxValueError:
        raise ValueError("yaml file is empty")  # Eğer YAML dosyası boşsa hata fırlatır.
    except Exception as e:
        raise e  # Diğer hataları yakalar ve fırlatır.
    
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)  # Belirtilen dizinleri oluşturur, varsa var olanları geçer.
        

@ensure_annotations
def get_size(path: Path) -> str:
    size_in_kb = round(os.path.getsize(path) / 1024)  # Dosyanın boyutunu KB cinsinden alır.
    return f"~ {size_in_kb} KB"  # Dosyanın boyutunu KB cinsinden döndürür.

@ensure_annotations
def save_object(file_path: Path, obj):
    try:
        dir_path = os.path.dirname(file_path)  # Dosya yolunu alır.
        os.makedirs(dir_path, exist_ok=True)  # Dosya yolu mevcut değilse oluşturur.
        with open(file_path, "wb") as file_obj:  # Dosyayı ikili (binary) modda açar.
            pickle.dump(obj, file_obj)  # Objeyi pickle ile kaydeder.
    except Exception as e:
        raise e  # Hata durumunda hatayı yakalar ve fırlatır.
        
    
def evaluate_model(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}  # Model değerlendirmesi için bir sözlük oluşturuluyor.
        for model_key in models:
            model = models[model_key]  # Modeli alır.
            para = param[model_key]  # Modelin hiperparametrelerini alır.
            gs = GridSearchCV(model, para, cv=3)  # GridSearchCV ile parametre araması yapar.
            
            gs.fit(X_train, y_train)  # GridSearchCV'yi eğitir.
            model.set_params(**gs.best_params_)  # En iyi parametrelerle model parametrelerini günceller.
            model.fit(X_train, y_train)  # Modeli yeniden eğitir.
            
            y_test_pred = model.predict(X_test)  # Test verisi üzerinde tahmin yapar.
            
            test_model_score = (
                r2_score(y_test, y_test_pred),  # R2 skorunu hesaplar.
                mean_absolute_error(y_test, y_test_pred),  # MAE hesaplar.
                mean_squared_error(y_test, y_test_pred)  # MSE hesaplar.
            )
            
            report[model_key] = test_model_score  # Model skorlarını rapora ekler.
            
        return report  # Raporu döndürür.
    
    except Exception as e:
        raise e  # Hata durumunda hatayı yakalar ve fırlatır.
    
    
    
@ensure_annotations
def save_transformed_data(data: Any, file_path: Path):
    """
    Veriyi belirtilen dosya yoluna kaydeder.
    
    :param data: Dönüştürülmüş veri (DataFrame)
    :param file_path: Verinin kaydedileceği dosya yolu
    """
    try:
        dir_path = os.path.dirname(file_path)  # Dosya yolunu alır.
        os.makedirs(dir_path, exist_ok=True)  # Dosya yolu mevcut değilse oluşturur.
        
        data.to_csv(file_path, index=False)  # Veriyi CSV formatında kaydeder.
        print(f"Veri başarıyla kaydedildi: {file_path}")  # Kaydedildiğine dair mesaj yazdırır.
        
    except Exception as e:
        raise e  # Hata durumunda hatayı yakalar ve fırlatır.