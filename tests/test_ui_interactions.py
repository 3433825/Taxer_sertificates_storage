import pytest
from playwright.sync_api import expect
from pages.main_page import MainPage


def test_active_state_and_details_order(page, preloaded_certs):
    main_page = MainPage(page)

    # Вибираємо імена з нашого списку попередньо завантажених сертифікатів
    first_cert = preloaded_certs[0]["name"]
    second_cert = preloaded_certs[1]["name"]

    # 1. Перевірка виділення та індикатора (BUG-11)
    main_page.get_cert_row(first_cert).click()

    # Перевіряємо наявність трикутника ► (Очікуємо падіння через BUG-11)
    assert main_page.check_active_indicator(
        first_cert
    ), f"BUG-11: Трикутник-індикатор (►) відсутній для {first_cert}"

    # 2. Перевірка перемикання деталей (TC-18)
    main_page.get_cert_row(second_cert).click()

    # Очікуємо, що в панелі деталей з'явиться ім'я другого власника
    expect(page.locator(".detail-panel")).to_contain_text(second_cert)

    # 3. Перевірка порядку полів у деталях (BUG-08)
    # Очікуваний порядок згідно з ТЗ
    expected_order = ["Common Name", "Issuer CN", "Valid From", "Valid To"]

    # Отримуємо фактичні назви полів з інтерфейсу
    labels = page.locator(".detail-field-label")
    actual_order = labels.all_text_contents()

    assert actual_order == expected_order, (
        f"BUG-08: Порядок або назви полів не збігаються. "
        f"Очікували: {expected_order}, отримали: {actual_order}"
    )
