import allure
from playwright.sync_api import expect
from pages.main_page import MainPage
from pages.upload_page import UploadPage
from utils.constants import CertConstants
from utils.logger import get_logger
from tests.config import Config

# Ініціалізуємо логер для повного відстеження E2E сценарію
logger = get_logger(__name__)


@allure.feature("End-to-End сценарії")
@allure.story("Повний життєвий цикл сертифіката (Завантаження -> Reload -> Деталі)")
@allure.severity(allure.severity_level.BLOCKER)
@allure.issue("E2E-01", "Перевірка цілісності даних та LocalStorage (Вимога 3)")
def test_e2e_certificate_full_lifecycle(page):
    """
    E2E Сценарій: Повний життєвий цикл сертифіката.
    Включає перевірку збереження даних після перезавантаження сторінки.
    """
    logger.info("--- ЗАПУСК ПОВНОГО E2E СЦЕНАРІЮ (End-to-End) ---")

    main_page = MainPage(page)
    upload_page = UploadPage(page)
    cert_name = CertConstants.VALID_OWNER
    valid_cert_path = Config.CERTS["valid"]["path"]

    with allure.step("1. Завантаження сертифіката через Drag-and-Drop"):
        logger.info("КРОК 1: Відкриття панелі завантаження та Drop файлу.")
        main_page.open_upload_screen()
        upload_page.upload_via_drop(valid_cert_path)

        # Повернення до списку
        upload_page.return_to_main()
        logger.info("Файл завантажено, повернуто до головного екрана.")

    with allure.step("2. Перезавантаження сторінки (Browser Reload)"):
        # Перевірка Вимоги 3: дані мають зберігатися в LocalStorage
        logger.info("КРОК 2: Повне перезавантаження сторінки.")
        page.reload()
        # Чекаємо стабілізації Angular додатка
        page.wait_for_load_state("networkidle")

    with allure.step(f"3. Верифікація наявності '{cert_name}' після оновлення"):
        logger.info("КРОК 3: Перевірка стійкості даних у списку.")
        target_cert = main_page.get_cert_by_name(cert_name)

        expect(
            target_cert,
            message=f"КРИТИЧНА ПОМИЛКА: Сертифікат {cert_name} зник після перезавантаження!",
        ).to_be_visible(timeout=10000)
        logger.info(f"Сертифікат '{cert_name}' успішно знайдено.")

    with allure.step("4. Перегляд деталей та Data Integrity"):
        logger.info("КРОК 4: Відкриття панелі деталей.")
        target_cert.click()

        # Перевіряємо відкриття таблиці
        expect(
            main_page.details_panel, message="Панель деталей не відкрилася після кліку"
        ).to_be_visible(timeout=5000)

        # Верифікація контенту (BUG-07/08)
        expect(main_page.details_panel).to_contain_text(cert_name)
        logger.info("Дані в панелі деталей відповідають завантаженому файлу.")

    with allure.step("5. Перевірка візуальних багів (BUG-11)"):
        logger.info("КРОК 5: Фіксація стану активності.")
        is_active = main_page.check_active_state(cert_name)

        if not is_active:
            # Використовуємо warning в логах, але в Allure це буде зафіксовано кроком
            logger.warning("BUG-11: Сертифікат не має класу 'active'.")
            allure.attach(
                "Bug-11 Detected", "Сертифікат не підсвічується у списку як активний."
            )
        else:
            logger.info("Сертифікат відображається коректно.")

    # Обов'язкове прибирання (Teardown) прямо в тесті, щоб не забивати LocalStorage
    with allure.step("Cleanup: Очищення LocalStorage"):
        page.evaluate("localStorage.clear()")
        logger.info("--- E2E СЦЕНАРІЙ ЗАВЕРШЕНО УСПІШНО ---")
