import os
from pathlib import Path
import logging

logging.basicConfig(level = logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = 'stok optimizasyonu ml project'

list_of_files = [
    ".github/workflows/.gitkeep", # bu dosyanın amacı sadece boş klasörlerin Git tarafından izlenmesini sağlamaktır.
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entitiy/__init__.py",
    f"src/{project_name}/entitiy/config_entitiy.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "app.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",
    "tamplates/index.html",
    "test.py"

]


for filepath in list_of_files:
    filepath = Path(filepath) # dosya yolunu Path objesine dönüştürür
    filedir,filename = os.path.split(filepath) # klasör yolunu ve dosya adını ayırır

    if filedir != "":  #eğer dosya yolu boş değilse
        os.makedirs(filedir,exist_ok=True) # Klasörü oluştur (zaten varsa hata vermez)
        logging.info(f"{filedir} dizini, {filename} dosyası için oluşturuluyor")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
    # Dosya mevcut değilse ya da boyutu sıfırsa, boş bir dosya oluşturuyoruz.
        with open(filepath, "w") as f:
            pass
            # burada dosya oluşturulurken bir log mesajı veriyoruz
            logging.info(f"Boş dosya oluşturuluyor: {filepath}")
    else:
        logging.info(f"{filename} zaten mevcut")