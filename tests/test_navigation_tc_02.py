import pytest
from playwright.sync_api import expect
from pages.main_page import MainPage
from pages.upload_page import UploadPage
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.xfail(reason="BUG: Текст інструкції в зоні drug&drop не відповідає ТЗ")
def test_navigation_to_upload_screen_tc02(page):
    """
    TC-02: Перевірка відкриття панелі завантаження.
    """
    logger.info("Запуск тесту TC-02: Перевірка відкриття панелі завантаження")
    main_page = MainPage(page)
    upload_page = UploadPage(page)

    # 1. Натискаємо "Завантажити" (BUG-01)
    main_page.open_upload_screen()

    # 2. ПЕРЕВІРКА: чи з'явилася панель завантаження
    # Тепер тест пройде, бо ми шукаємо саме .dropbox-panel
    expect(
        main_page.drop_panel, message="Панель завантаження не з'явилася"
    ).to_be_visible(timeout=5000)

    # 3. ПЕРЕВІРКА вмісту панелі (Вимога 5)
    # Перевіряємо текст інструкції всередині зони
    expect(
        upload_page.drop_zone,
        message="Текст інструкції в зоні drug&drop не відповідає ТЗ",
    ).to_contain_text(UploadPage.instruction_text)

    # 4. ФІКСАЦІЯ BUG-05 (Відсутність кнопки "Вибрати")
    # ТЗ вимагає кнопку "Вибрати", але на drop_zone.png її немає
    select_btn = page.get_by_role("button", name="Вибрати")
    assert select_btn.is_hidden(), "BUG-05: Кнопка 'Вибрати' все ще відсутня"
