import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = os.getenv("BASE_URL")
    # Динамічно отримуємо абсолютні шляхи до .cer файлів

    CERT_VALID = os.path.abspath(os.getenv("CERT_VALID") or "data/valid_cert.cer")
    CERT_EXPIRED = os.path.abspath(os.getenv("CERT_EXPIRED") or "data/expired.cer")

    CERTS = {
        "valid": {"path": CERT_VALID, "owner": "Олег Андрійович"},
        "expired": {"path": CERT_EXPIRED},
    }
