import allure
from playwright.sync_api import expect
from pages.main_page import MainPage
from pages.upload_page import UploadPage
from utils.constants import CertConstants
from utils.logger import get_logger
from tests.config import Config

logger = get_logger(__name__)


@allure.feature("Завантаження сертифікатів")
@allure.story("Успішне додавання .cer файлу")
@allure.severity(allure.severity_level.CRITICAL)
@allure.issue("TC-05", "Додавання сертифікату через Drag-and-Drop")
def test_successful_certificate_upload_tc05(page):
    """
    TC-05: Додавання сертифікату.
    Перевіряє, що після імітації Drag-and-Drop файлу .cer
    сертифікат з'являється в загальному списку.
    """
    logger.info("--- ЗАПУСК TC-05: Додавання сертифікату ---")

    main_page = MainPage(page)
    upload_page = UploadPage(page)
    expected_name = CertConstants.VALID_OWNER
    valid_cert_path = Config.CERTS["valid"]["path"]

    with allure.step("1. Відкриття панелі завантаження"):
        main_page.open_upload_screen()
        logger.info("Панель завантаження відкрита.")

    with allure.step(f"2. Завантаження сертифікату через JS-drop: {valid_cert_path}"):
        # Обхід BUG-05 (відсутність кнопки 'Вибрати')
        upload_page.upload_via_drop(valid_cert_path)

    with allure.step("3. Повернення до головного екрану"):
        upload_page.return_to_main()

    with allure.step(f"4. Верифікація появи сертифіката: {expected_name}"):
        logger.info(f"Очікуємо появу сертифіката: {expected_name}")
        target_cert = main_page.get_cert_by_name(expected_name)

        expect(
            target_cert,
            message=f"Сертифікат '{expected_name}' не знайдено в списку після завантаження",
        ).to_be_visible(timeout=10000)

    logger.info("--- TC-05 ЗАВЕРШЕНО УСПІШНО ---")
