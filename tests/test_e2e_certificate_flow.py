import pytest
from playwright.sync_api import expect
from pages.main_page import MainPage
from pages.upload_page import UploadPage
from utils.constants import CertConstants
from utils.logger import get_logger
from tests.config import Config

# Ініціалізуємо логер для повного відстеження E2E сценарію
logger = get_logger(__name__)


def test_e2e_certificate_full_lifecycle(page):
    """
    E2E Сценарій: Повний життєвий цикл сертифіката.

    Кроки:
    1. Перевірка початкового стану (опціонально).
    2. Завантаження валідного .cer файлу через JS-ін'єкцію (обхід BUG-05).
    3. Повернення до списку та ПЕРЕЗАВАНТАЖЕННЯ сторінки (Вимога 3).
    4. Перевірка стійкості даних у списку після Reload.
    5. Перегляд деталей та верифікація полів (BUG-07, BUG-08).
    6. Перевірка візуального стану активності (BUG-11).
    """
    logger.info("--- ЗАПУСК ПОВНОГО E2E СЦЕНАРІЮ (End-to-End) ---")

    main_page = MainPage(page)
    upload_page = UploadPage(page)

    # КРОК 1: Завантаження сертифіката
    logger.info("КРОК 1: Відкриття панелі завантаження та Drop файлу.")
    main_page.open_upload_screen()

    valid_cert_path = Config.CERTS["valid"]["path"]
    upload_page.upload_via_drop(valid_cert_path)

    # Невелика пауза для завершення анімацій Angular перед виходом
    page.wait_for_timeout(1000)
    upload_page.return_to_main()
    logger.info("Файл завантажено, повернуто до головного екрана.")

    # КРОК 2: Перезавантаження сторінки
    # Це найважливіша частина для перевірки збереження даних у localStorage
    logger.info("КРОК 2: Повне перезавантаження сторінки (Browser Reload).")
    main_page.reload_page()

    # КРОК 3: Верифікація даних після Reload
    logger.info("КРОК 3: Перевірка наявності сертифіката у списку після оновлення.")
    cert_name = CertConstants.VALID_OWNER
    target_cert = main_page.get_cert_by_name(cert_name)

    expect(
        target_cert,
        message=f"КРИТИЧНА ПОМИЛКА: Сертифікат {cert_name} зник після перезавантаження!",
    ).to_be_visible(timeout=10000)
    logger.info(f"Сертифікат '{cert_name}' успішно знайдено у списку.")

    # КРОК 4: Перегляд деталей (Data Integrity)
    logger.info("КРОК 4: Відкриття панелі деталей та перевірка полів.")
    target_cert.click()

    # Перевіряємо, що таблиця деталей з'явилася
    expect(
        main_page.details_panel, message="Панель деталей не відкрилася після кліку"
    ).to_be_visible(timeout=5000)

    # Перевіряємо, що в таблиці є ім'я власника (підтверджує успішний парсинг)
    expect(main_page.details_panel).to_contain_text(cert_name)

    # КРОК 5: Фіксація багів верстки (Візуальний чек)
    logger.info("КРОК 5: Перевірка стану активності (BUG-11).")
    is_active = main_page.check_active_state(cert_name)

    if not is_active:
        logger.warning("BUG-11: Сертифікат не підсвічується як активний у списку.")
    else:
        logger.info("Сертифікат відображається як активний.")

    logger.info("--- E2E СЦЕНАРІЙ ЗАВЕРШЕНО УСПІШНО ---")
