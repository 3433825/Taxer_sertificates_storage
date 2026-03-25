import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = os.getenv("BASE_URL")
    # Динамічно отримуємо абсолютні шляхи до .cer файлів
    CERT_VALID = os.path.abspath(os.getenv("CERT_VALID"))
    CERT_EXPIRED = os.path.abspath(os.getenv("CERT_EXPIRED"))
    CERT_LONG_NAME = os.path.abspath(os.getenv("CERT_LONG_NAME"))
    CERT_BROKEN = os.path.abspath(os.getenv("CERT_BROKEN"))

    # Додаємо цей блок, якого не вистачає:
    CERTS = {
        "valid": {"path": os.path.abspath(os.getenv("CERT_VALID", "data/valid.cer"))},
        "expired": {
            "path": os.path.abspath(os.getenv("CERT_EXPIRED", "data/expired.cer"))
        },
    }
