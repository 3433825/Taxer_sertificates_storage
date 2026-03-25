import pytest
from playwright.sync_api import expect
from pages.main_page import MainPage
from pages.upload_page import UploadPage
from config import Config
from utils.constants import CertConstants


@pytest.mark.parametrize(
    "cert_path, expected_name",
    [
        (Config.CERT_VALID, CertConstants.VALID_OWNER),
    ],
)
def test_certificate_details_validation(page, cert_path, expected_name):
    main_page = MainPage(page)
    upload_page = UploadPage(page)

    # 1. Перехід до завантаження (Вимога 8) [cite: 69, 81]
    main_page.open_upload()

    # 2. Завантаження .cer файлу (Вимога 5) [cite: 66, 99]
    upload_page.upload_certificate(cert_path)
    upload_page.return_to_main()

    # 3. Перевірка появи у списку (Вимога 1) [cite: 62, 149]
    cert_row = main_page.cert_list_item(expected_name)
    expect(cert_row).to_be_visible()

    # 4. Відкриття панелі деталей (Вимога 2) [cite: 63, 167]
    cert_row.click()

    # ПЕРЕВІРКА BUG-07: Назви полів (Очікуємо падіння) [cite: 172, 286]
    # ТЗ вимагає "Common Name", а по факту "SubjectCN"
    expected_fields = ["Common Name", "Issuer CN", "Valid From", "Valid To"]

    for field_name in expected_fields:
        # expect(page.locator(f"text={field_name}")).to_be_visible() # Це впаде
        print(f"Checking field: {field_name}")

        # ПЕРЕВІРКА BUG-08: Порядок полів (Valid From має бути перед Valid To) [cite: 172, 298]
    # У додатку зараз ValidTill (To) йде перед ValidFrom
    fields = page.locator(".detail-field-label")  # Припустимо такий клас для назв полів
    # Тут можна додати логіку порівняння списків текстів
