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
from typing import List


@ensure_annotations # Bu fonksiyon, bir YAML dosyasını okuyup, içeriğini bir Box nesnesi olarak döndürür.
def read_yaml(path_to_yaml: Path) -> Box:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)  # YAML içeriğini okur python sözlük tipine çevirir

            if content is None:  # Eğer YAML dosyası boşsa
                raise ValueError("YAML file is empty") # boşsa hata fırlatır

            return Box(content)  # Box nesnesi olarak döndür yani keylere direk data.sütun olarak ulaşabiliriz
    except Exception as e:
        raise e  # Diğer hataları yakala ve fırlat
        
    
    
@ensure_annotations # path_to_directories listesindeki her yolu alır ve klasör oluşturur.
def create_directories(path_to_directories: List[str], verbose=True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            print(f"Directory created: {path}")  # Yeni dizin oluşturulduğunda mesaj yazdır.



@ensure_annotations # Bu fonksiyon, bir dosyanın boyutunu KB (kilobayt) cinsinden döndürür.
def get_size(path: Path) -> str:
    size_in_kb = round(os.path.getsize(path) / 1024)  # Dosyanın boyutunu KB cinsinden alır.
    return f"~ {size_in_kb} KB"  # Dosyanın boyutunu KB cinsinden döndürür.



@ensure_annotations # Bu fonksiyon, Python objelerini (dictionary, liste, model vb.) pickle formatında kaydeder.
def save_object(file_path: Path, obj): # file_path: Path → Kaydedilecek dosyanın yolu.obj → Kaydedilecek Python nesnesi (örneğin bir sözlük, model, veri çerçevesi vb.).
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
def save_transformed_data(data: Any, file_path: Path, format: str = "csv"): # belirtilen veriyi (data parametresi) ve dosya yolunu (file_path parametresi) alarak, veriyi belirtilen formatta (CSV ya da JSON) kaydetmek için kullanılır.
    try:
        dir_path = os.path.dirname(file_path)  # Dosya yolunun dizin kısmını alır.
        os.makedirs(dir_path, exist_ok=True)  # Eğer dosyanın bulunduğu dizin mevcut değilse, dizini oluşturur.

        if format == "csv":  # Eğer format "csv" olarak verilmişse
            data.to_csv(file_path, index=False)  # Veriyi CSV formatında belirtilen dosyaya kaydeder (index'i kaydetmeden).
        elif format == "json":  # Eğer format "json" olarak verilmişse
            data.to_json(file_path, orient="records", indent=4)  # Veriyi JSON formatında kaydeder, her kayıt yeni bir satıra yazılır.
        else:
            raise ValueError(f"Geçersiz format: {format}")  # Eğer format ne CSV ne de JSON ise, hata fırlatır.

        print(f"Veri başarıyla kaydedildi: {file_path}")  # Verinin başarıyla kaydedildiğini belirten mesajı yazdırır.

    except Exception as e:  # Eğer bir hata oluşursa
        raise RuntimeError(f"Veri kaydedilirken hata oluştu: {e}")  # Hata mesajıyla birlikte RuntimeError fırlatır.