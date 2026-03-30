from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class MainPage(BasePage):
    """
    Клас для взаємодії з головною сторінкою (список сертифікатів).
    """

    def __init__(self, page):
        super().__init__(page)

        # СЕЛЕКТОРИ
        # BUG-01: Текст кнопки "Завантажити" замість "Додати"
        self.add_button = page.locator("button.btn-primary:has-text('Завантажити')")

        # Елементи списку сертифікатів
        self.cert_items = page.locator("a.list-group-item")

        # Панель завантаження
        self.drop_panel = page.locator(".dropbox-panel")

        # Текст повідомлення про порожній стан (Вимога 1)
        self.empty_state_msg = page.get_by_text("Нема жодного сертифікату")

        # Панель деталей (з'являється праворуч після кліку на сертифікат)
        self.details_panel = page.locator("table.table-borderless")

        # Назви полів у таблиці деталей (Common Name, Issuer CN тощо)
        self.detail_labels = self.details_panel.locator("th")

        # Значення полів
        self.detail_values = self.details_panel.locator("td")

    def open_upload_screen(self):
        """Відкриває панель завантаження."""
        logger.info("Натискання кнопки 'Завантажити' для відкриття панелі.")
        self.add_button.click()
        self.drop_panel.wait_for(state="visible", timeout=5000)

    def get_cert_by_name(self, name: str):
        """Повертає локатор конкретного сертифіката у списку за його ім'ям."""
        logger.info(f"Пошук локатора для сертифіката: {name}")
        # Використовуємо filter для точного пошуку по тексту всередині елемента
        return self.cert_items.filter(has_text=name)

    def get_details_headers(self) -> list:
        """
        Отримує список усіх заголовків (назв полів) з таблиці деталей.
        Використовується в TC-18 для перевірки BUG-08 (порядок полів).
        """
        # Чекаємо, поки панель деталей стане видимою
        self.details_panel.wait_for(state="visible", timeout=5000)

        # .all_text_contents() повертає список рядків (текст кожного <th>)
        headers = self.detail_labels.all_text_contents()

        # Очищуємо текст від зайвих пробілів та двокрапок (якщо вони є в верстці)
        clean_headers = [h.strip().replace(":", "") for h in headers if h.strip()]

        logger.info(f"Отримано заголовки деталей: {clean_headers}")
        return clean_headers

    # --- АЛІАСИ ТА ДОПОМІЖНІ МЕТОДИ ---

    def is_cert_in_list(self, name: str) -> bool:
        count = self.get_cert_by_name(name).count()
        return count > 0

    def check_active_state(self, name: str) -> bool:
        target = self.get_cert_by_name(name)
        classes = target.get_attribute("class") or ""
        return "active" in classes

    def open_upload(self):
        self.open_upload_screen()

    def get_cert_row(self, name: str):
        return self.get_cert_by_name(name)
