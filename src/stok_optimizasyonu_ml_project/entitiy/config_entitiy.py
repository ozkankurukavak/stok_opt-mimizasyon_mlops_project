from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path
 

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    transformed_data_path: Path  # Yeni eklenen kısım


@dataclass
class ModelTrainerConfig:
    root_dir: Path                          # Modelin kaydedileceği ana dizin
    train_data_path: Path                    # Eğitim verisinin yolu
    test_data_path: Path                     # Test verisinin yolu
    model_name: str                          # Modelin adı (Örneğin: "xgboost_model.pkl")
    target_column: str                       # Hedef değişkenin adı
    xgboost_params: Dict[str, Any]           # XGBoost parametrelerini burada saklayacağız
    grid_search: bool = True                 # Grid search uygulanacak mı?
    scoring_metric: str = "accuracy"         # Skor metrici, doğruluk için "accuracy" kullanılabilir
    test_size: float = 0.2                   # Test seti boyutu, genellikle 0.2 ya da 0.3 kullanılır
    random_state: int = 42            