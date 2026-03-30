import allure
import pytest
from playwright.sync_api import expect
from pages.main_page import MainPage
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("Деталі сертифікату")
@pytest.mark.xfail(
    reason="BUG-08: Порядок та назви полів не відповідають ТЗ (Вимога 8)"
)
@allure.story("Перевірка порядку полів у деталях")
@allure.severity(allure.severity_level.NORMAL)
@allure.issue("TC-18", "Відповідність порядку полів у таблиці деталей (Вимога 8)")
def test_certificate_details_order_tc18(page, preloaded_certs):
    """
    TC-18: Перевірка порядку полів у деталях сертифікату.

    Кроки:
    1. Використовує фікстуру preloaded_certs для підготовки даних.
    2. Вибирає завантажений сертифікат зі списку.
    3. Отримує список заголовків у таблиці деталей.
    4. Порівнює фактичний порядок із еталонним згідно з ТЗ.
    """
    logger.info("--- ЗАПУСК TC-18: Перевірка порядку полів у деталях ---")

    main_page = MainPage(page)

    # Еталонний порядок полів згідно з Технічним Завданням (Вимога 8)
    ideal_order = ["Common Name", "Issuer CN", "Valid From", "Valid To"]

    # Отримуємо ім'я сертифіката, який завантажила фікстура
    expected_name = preloaded_certs[0]["name"]

    with allure.step(f"1. Вибір сертифіката зі списку: {expected_name}"):
        logger.info(f"Шукаємо та клікаємо по сертифікату: {expected_name}")
        cert_item = main_page.get_cert_by_name(expected_name)

        # Додаткова перевірка видимості перед кліком для стабільності
        expect(cert_item).to_be_visible(timeout=5000)
        cert_item.click()

    with allure.step("2. Отримання фактичного списку полів з таблиці деталей"):
        # Метод get_details_headers має повертати список текстів заголовків (TH або TD)
        actual_fields = main_page.get_details_headers()
        logger.info(f"Отримано фактичні поля: {actual_fields}")

    with allure.step("3. Верифікація порядку полів (BUG-08)"):
        # Якщо порядок не збігається, тест впаде з детальним описом для Allure
        assert actual_fields == ideal_order, (
            f"BUG-08: Порядок полів у деталях не відповідає ТЗ. \n"
            f"Очікувано: {ideal_order}\n"
            f"Фактично: {actual_fields}"
        )

    logger.info("--- TC-18 ЗАВЕРШЕНО УСПІШНО ---")
