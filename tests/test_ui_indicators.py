import pytest
from playwright.sync_api import expect
from pages.main_page import MainPage
from config import Config

def test_active_certificate_indicator_bug(page):
    main_page = MainPage(page)
    cert_name = "Олег Андрійович (Тест)" # З вашого списку [cite: 153]

    # Припускаємо, що один сертифікат вже є (або завантажуємо його)
    # Клікаємо на сертифікат [cite: 167, 172]
    main_page.get_cert_row(cert_name).click()

    # Верифікація BUG-11 [cite: 322]
    # Очікуємо, що індикатор '►' видимий.
    # Тест впаде, бо фактично його немає[cite: 333].
    assert main_page.check_active_indicator(cert_name), (
        "BUG-11: Трикутник-індикатор (►) відсутній біля активного запису"
    )
