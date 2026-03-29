import pytest
import allure
from playwright.sync_api import expect
from pages.main_page import MainPage
from pages.upload_page import UploadPage
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("Навігація")
@allure.story("Відкриття екрану завантаження")
@allure.severity(allure.severity_level.CRITICAL)
@allure.issue("TC-02", "Вимога 8 — Коректна навігація між екранами")
@pytest.mark.xfail(reason="BUG: Текст інструкції в зоні drug&drop не відповідає ТЗ")
def test_navigation_to_upload_screen_tc02(page):
    """
    TC-02: Перевірка відкриття панелі завантаження.
    """
    logger.info("Запуск тесту TC-02: Перевірка відкриття панелі завантаження")
    main_page = MainPage(page)
    upload_page = UploadPage(page)

    with allure.step("1. Натискання кнопки 'Завантажити'"):
        main_page.open_upload_screen()

    with allure.step("2. Перевірка появи панелі завантаження"):
        # Перевіряємо видимість панелі згідно з Вимогою 8 [cite: 53]
        expect(
            main_page.drop_panel, message="Панель завантаження не з'явилася"
        ).to_be_visible(timeout=5000)

    with allure.step("3. Перевірка тексту інструкції в зоні Drag&Drop"):
        # Очікуваний текст з Вимоги 7: "Перетягніть файл сертифікату сюди або"
        expect(
            upload_page.drop_zone,
            message="Текст інструкції в зоні drug&drop не відповідає ТЗ",
        ).to_contain_text(upload_page.instruction_text)

    with allure.step("4. Перевірка наявності кнопки 'Вибрати'"):
        # Фіксація BUG-05: Кнопка відсутня, хоча має бути згідно з Вимогою 7
        select_btn = page.get_by_role("button", name="Вибрати")
        assert select_btn.is_hidden(), "BUG-05: Кнопка 'Вибрати' все ще відсутня"
