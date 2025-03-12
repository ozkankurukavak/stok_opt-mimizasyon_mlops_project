import pandas as pd
import os
from src.stok_optimizasyonu_ml_project import logger
from sklearn.model_selection import GridSearchCV
import xgboost as xgb
import joblib
from sklearn.metrics import mean_squared_error
from src.stok_optimizasyonu_ml_project.entitiy.config_entitiy import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        # Eğitim ve test verilerini yükle
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)
        
        # Eğitim verisinden örnekleme yap
        train_data_sample = train_data.sample(frac=0.1, random_state=42)  # Verinin %10'u ile eğitim
        
        # X ve y'yi ayır
        X_train = train_data_sample.drop(self.config.target_column, axis=1)
        y_train = train_data_sample[self.config.target_column]
        X_test = test_data.drop(self.config.target_column, axis=1)
        y_test = test_data[self.config.target_column]

        # XGBoost modelini oluştur
        xgb_model = xgb.XGBRegressor(n_jobs = -1)

        # Parametre ızgarası
        param_grid = {
            'n_estimators': self.config.xgboost_params['n_estimators'],
            'max_depth': self.config.xgboost_params['max_depth'],
            'learning_rate': self.config.xgboost_params['learning_rate'],
            'subsample': self.config.xgboost_params['subsample'],
        }

        # GridSearchCV ile parametre araması yapalım
        grid_search = GridSearchCV(xgb_model, param_grid, cv=3, verbose=1)
        grid_search.fit(X_train, y_train)

        # En iyi parametreyi al
        best_model = grid_search.best_estimator_

        # Modeli test et
        y_pred = best_model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f'Mean Squared Error: {mse}')

        # Modeli kaydet
        joblib.dump(best_model, os.path.join(self.config.root_dir, self.config.model_name))