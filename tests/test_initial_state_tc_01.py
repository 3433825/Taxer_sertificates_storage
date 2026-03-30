import pytest
import allure
from playwright.sync_api import expect
from pages.main_page import MainPage


@allure.feature("Стартова сторінка")
@allure.story("Перевірка порожнього стану")
@allure.severity(allure.severity_level.CRITICAL)
@allure.issue("TC-01", "Вимога 7 — Відповідність елементів інтерфейсу макетам")
@pytest.mark.xfail(
    reason="BUG: Відсутня інструкція 'Нема жодного сертифікату' згідно з Вимогою 1"
)
def test_initial_empty_state_tc01(page):
    main_page = MainPage(page)

    with allure.step("Перевірка, що список сертифікатів порожній"):
        # Очікуємо 0 елементів у списку
        expect(main_page.cert_items).to_have_count(0)

    with allure.step("Перевірка наявності кнопки додавання"):
        # Кнопка має бути видимою, хоча ми знаємо про BUG-01 з назвою
        expect(main_page.add_button).to_be_visible()

    with allure.step("Перевірка відображення тексту-заглушки"):
        # Очікуємо текст «Нема жодного сертифікату» [cite: 7, 63]
        # Тест впаде тут, Allure зробить скріншот автоматично завдяки нашому hook у conftest.py
        expect(main_page.empty_state_msg).to_be_visible(timeout=5000)
