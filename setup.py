import setuptools  # Setuptools kütüphanesini import ediyoruz, Python paketleri oluşturmak için kullanılır.

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()  # README.md dosyasını açıp, içeriğini 'long_description' değişkenine okuyoruz.
    # README dosyası, paket hakkında açıklama ve bilgi içerir.

__version__ = "0.0.0"  # Paket sürümünü tanımlıyoruz.

REPO_NAME = "stok-optimizasyon_mlops-project-with-DVC-Mlflow"  # Repo ismini tanımlıyoruz.
AUTHOR_USER_NAME = "özkan"  # Yazar adı.
SRC_REPO = "mlproject"  # Kaynak proje adı.
AUTHOR_EMAIL = "kurukavakozkan57@gmail.com"  # Yazar e-posta adresi.


setuptools.setup(  # Setuptools setup fonksiyonunu çağırıyoruz, burada paket yapılandırmasını yapıyoruz.
    name=SRC_REPO,  # Paket ismi.
    version=__version__,  # Paket sürümü.
    author=AUTHOR_USER_NAME,  # Yazar adı.
    author_email=AUTHOR_EMAIL,  # Yazar e-posta adresi.
    description="stok optimizasyonu mlops projesi",  # Kısa paket açıklaması.
    long_description=long_description,  # Uzun açıklama, genellikle README dosyasından alınır.
    long_description_content="text/markdown",  # Uzun açıklamanın biçimi, markdown formatında olduğu belirtilir.
    url=f"https://github.com/ozkankurukavak/stok_opt-mimizasyon_mlops_project",  # Paket için URL, burada GitHub reposunun bağlantısı.
    project_urls={  # Projeye ilişkin ekstra bağlantılar.
        "Bug Tracker:": f"https://github.com/ozkankurukavak/stok_opt-mimizasyon_mlops_project/issues",  # Hata takibi (bug tracker) linki.
    },
    package_dir={"": "src"},  # Paketlerin bulunduğu dizin, 'src' altında paketler aranacak.
    packages=setuptools.find_packages(where="src")  # 'src' dizininde yer alan tüm Python paketlerini buluyoruz.
)