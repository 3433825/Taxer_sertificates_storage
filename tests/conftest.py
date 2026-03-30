import allure
import pytest
from pages.base_page import BasePage
from pages.main_page import MainPage
from pages.upload_page import UploadPage
from utils.constants import CertConstants
from utils.logger import get_logger
from config import Config

# Ініціалізуємо логер для фікстур
logger = get_logger(__name__)


@pytest.fixture(autouse=True)
def setup_and_teardown(page):
    """
    Базова фікстура: готує чистий додаток перед кожним тестом.
    Виконується автоматично завдяки autouse=True.
    """
    logger.info("=== ПІДГОТОВКА СЕРЕДОВИЩА (Setup) ===")
    base_page = BasePage(page)

    # 1. Відкриваємо сайт та проходимо StackBlitz
    base_page.navigate()

    # 2. Очищуємо LocalStorage (Вимога 3)
    base_page.clear_local_storage()

    # 3. Перезавантажуємо, щоб додаток побачив порожнє сховище
    base_page.reload_page()

    logger.info("=== СЕРЕДОВИЩЕ ГОТОВЕ ДО ТЕСТУ ===")
    yield
    logger.info("=== ЗАВЕРШЕННЯ ТЕСТУ (Teardown) ===")


@pytest.fixture
def preloaded_certs(page):
    """
    Фікстура-наповнювач: завантажує сертифікати перед початком тесту.
    Використовує upload_via_drop (Fix для 05_08).
    """
    main_page = MainPage(page)
    upload_page = UploadPage(page)

    certs_to_upload = [
        {"path": Config.CERTS["valid"]["path"], "name": CertConstants.VALID_OWNER}
    ]

    # --- SETUP ---
    with allure.step("Setup: Попереднє завантаження сертифікатів через фікстуру"):
        logger.info("Початок попереднього завантаження сертифікатів...")

        for cert in certs_to_upload:
            with allure.step(f"Завантаження: {cert['name']}"):
                main_page.open_upload_screen()
                upload_page.upload_via_drop(cert["path"])
                # Замість wait_for_timeout краще чекати на повернення кнопки
                upload_page.return_to_main()

        logger.info("Фікстура успішно підготувала дані.")

    yield certs_to_upload  # Тест отримує дані тут

    # --- TEARDOWN ---
    with allure.step("Teardown: Очищення LocalStorage після тесту"):
        logger.info("Очищення даних для ізоляції наступного тесту")
        page.evaluate("localStorage.clear()")
        page.reload()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Перевіряємо, чи тест впав під час виконання
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            # Робимо скріншот і додаємо в Allure
            allure.attach(
                page.screenshot(full_page=True),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )
