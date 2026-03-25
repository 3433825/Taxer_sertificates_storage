from .base_page import BasePage
from utils.logger import get_logger

# Ініціалізуємо логер для відстеження дій на головній сторінці
logger = get_logger(__name__)


class MainPage(BasePage):
    """
    Клас для взаємодії з головною сторінкою (список сертифікатів).
    Охоплює функціонал перегляду списку та відкриття панелі завантаження.
    """

    def __init__(self, page):
        super().__init__(page)

        # СЕЛЕКТОРИ (на основі storage_.png)
        # BUG-01: Текст кнопки "Завантажити" замість "Додати"
        self.add_button = page.locator("button.btn-primary:has-text('Завантажити')")

        # Елементи списку сертифікатів (<a> теги з ng-repeat)
        self.cert_items = page.locator("a.list-group-item")

        # Панель завантаження (з'являється при кліку на add_button)
        self.drop_panel = page.locator(".dropbox-panel")

        # Текст повідомлення про порожній стан (Вимога 1)
        self.empty_state_msg = page.get_by_text("Нема жодного сертифікату")

        # Панель деталей (з'являється праворуч після кліку на сертифікат)
        self.details_panel = page.locator("table.table-borderless")
        # Назви полів (Common Name, Issuer CN тощо)
        self.detail_labels = page.locator("th")
        # Значення полів
        self.detail_values = page.locator("td")

    def open_upload_screen(self):
        """
        Відкриває панель завантаження через клік по головній кнопці.
        """
        logger.info("Натискання кнопки 'Завантажити' для відкриття панелі.")
        self.add_button.click()
        # Чекаємо появи панелі, щоб переконатися, що Angular відпрацював ng-show
        self.drop_panel.wait_for(state="visible", timeout=5000)

    def get_cert_by_name(self, name: str):
        """
        Повертає локатор конкретного сертифіката у списку за його ім'ям.

        Args:
            name (str): Ім'я власника (Common Name), яке відображається у списку.
        """
        logger.info(f"Пошук локатора для сертифіката: {name}")
        return self.cert_items.filter(has_text=name)

    def is_cert_in_list(self, name: str) -> bool:
        """
        Перевіряє фізичну наявність сертифіката у DOM-дереві списку.

        Returns:
            bool: True, якщо знайдено хоча б один такий елемент.
        """
        count = self.get_cert_by_name(name).count()
        logger.info(f"Перевірка наявності '{name}': знайдено {count} шт.")
        return count > 0

    def check_active_state(self, name: str) -> bool:
        """
        Перевіряє, чи є сертифікат вибраним (активним) через клас CSS.
        Корисно для перевірки BUG-11.
        """
        target = self.get_cert_by_name(name)
        classes = target.get_attribute("class") or ""
        is_active = "active" in classes
        logger.info(f"Сертифікат '{name}' має статус active: {is_active}")
        return is_active

    def open_upload(self):
        """Аліас для open_upload_screen, який очікує тест"""
        self.open_upload_screen()

    def get_cert_row(self, name: str):
        """Метод, який очікує тест для кліку по сертифікату"""
        return self.get_cert_by_name(name)

    def check_active_indicator(self, name: str) -> bool:
        """
        Перевірка BUG-11: пошук символу '►' всередині активного елемента.
        """
        target = self.get_cert_by_name(name)
        # Шукаємо текст стрілочки всередині конкретного рядка
        indicator = target.locator("span:has-text('►')")
        is_visible = indicator.is_visible()
        logger.info(f"Індикатор '►' для '{name}' видимий: {is_visible}")
        return is_visible
