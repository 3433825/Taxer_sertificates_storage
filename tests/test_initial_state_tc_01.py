import pytest
from playwright.sync_api import expect
from pages.main_page import MainPage


@pytest.mark.xfail(
    reason="BUG: Відсутня інструкція 'Нема жодного сертифікату' згідно з Вимогою 1"
)
def test_initial_empty_state_tc01(page):
    main_page = MainPage(page)

    expect(main_page.cert_items).to_have_count(0)

    expect(main_page.add_button).to_be_visible()

    expect(main_page.empty_state_msg).to_be_visible(timeout=5000)
