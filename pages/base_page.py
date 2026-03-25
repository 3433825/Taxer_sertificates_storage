from playwright.sync_api import Page, TimeoutError
from tests.config import Config
from utils.logger import get_logger

# Ініціалізуємо логер для цього класу
logger = get_logger(__name__)


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        # Елементи системного захисту StackBlitz
        self.sb_run_button = page.get_by_role("button", name="Run this project")

    def navigate(self):
        """Відкриває URL та проходить через екран захисту StackBlitz."""
        logger.info(f"Відкриття сторінки: {Config.BASE_URL}")
        try:
            self.page.goto(Config.BASE_URL)
            self.page.wait_for_load_state("networkidle")
            self.bypass_stackblitz()
        except Exception as e:
            logger.error(f"Не вдалося перейти за посиланням: {e}")
            raise

    def bypass_stackblitz(self):
        """Метод для натискання синьої кнопки захисту StackBlitz."""
        logger.info("Перевірка наявності захисного екрана StackBlitz...")
        try:
            # Чекаємо появи кнопки 10 секунд
            self.sb_run_button.wait_for(state="visible", timeout=10000)
            logger.info("Кнопка 'Run this project' знайдена. Натискаю...")
            self.sb_run_button.click(force=True)

            # Чекаємо, поки кнопка зникне (додаток почав завантаження)
            self.sb_run_button.wait_for(state="hidden", timeout=7000)
            logger.info("Захист StackBlitz успішно пройдено.")
        except TimeoutError:
            logger.info("Екран захисту не з'явився або вже був пройдений.")
        except Exception as e:
            logger.warning(f"Виникла затримка при обході StackBlitz: {e}")

    def wait_for_app_load(self, selector: str = "button.btn-primary"):
        """Очікує появи головних елементів додатка (напр. синьої кнопки)."""
        logger.info(f"Очікування завантаження інтерфейсу (селектор: {selector})...")
        try:
            self.page.wait_for_selector(selector, timeout=15000)
            logger.info("Додаток готовий до роботи.")
        except TimeoutError:
            logger.error("Додаток не завантажився вчасно. Робимо скріншот.")
            self.page.screenshot(path="logs/app_load_error.png")
            raise

    def clear_local_storage(self):
        """Очищення сховища браузера для чистоти тестів (Вимога 3)."""
        logger.info("Очищення window.localStorage...")
        self.page.evaluate("window.localStorage.clear();")

    def reload_page(self):
        """Повне перезавантаження для застосування змін у сховищі."""
        logger.info("Перезавантаження сторінки...")
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        self.bypass_stackblitz()
        self.wait_for_app_load()

    def get_text(self, selector: str) -> str:
        """Зручний метод для отримання очищеного тексту елемента."""
        text = self.page.locator(selector).inner_text()
        return text.strip() if text else ""
