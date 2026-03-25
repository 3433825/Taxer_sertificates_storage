import os

from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class UploadPage(BasePage):
    """
    Клас для взаємодії з панеллю завантаження сертифікатів.
    Оскільки стандартний input[type='file'] відсутній (BUG-05),
    використовується імітація події Drag-and-Drop через JavaScript.
    """

    def __init__(self, page):
        super().__init__(page)
        self.drop_zone_selector = "dropbox.dropbox"
        self.drop_zone = page.locator("dropbox.dropbox")
        self.back_button = page.locator("button:has-text('Back')")

    def upload_via_drop(self, file_path: str):
        """
        Імітує перетягування файлу через JS. Виправлено передачу аргументів.
        """
        if not os.path.exists(file_path):
            logger.error(f"Файл не знайдено: {file_path}")
            raise FileNotFoundError(f"Тестовий файл відсутній: {file_path}")

        file_name = os.path.basename(file_path)
        logger.info(f"Початок імітації drop для: {file_name}")

        with open(file_path, "rb") as f:
            file_content = list(f.read())

        # Оновлений скрипт: тепер аргументи приходять як об'єкт
        js_drop_script = """
        async (args) => {
            const { selector, fileName, content } = args;

            const element = document.querySelector(selector);
            if (!element) {
                console.error('Елемент не знайдено:', selector);
                return;
            }

            const buffer = new Uint8Array(content).buffer;
            const file = new File([buffer], fileName, { type: 'application/x-x509-ca-cert' });

            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);

            const event = new DragEvent('drop', {
                dataTransfer,
                bubbles: true,
                cancelable: true
            });

            element.dispatchEvent(event);
            console.log('Подію drop імітовано для:', fileName);
        }
        """

        try:
            # Передаємо аргументи як ОДИН словник (args)
            payload = {
                "selector": self.drop_zone_selector,
                "fileName": file_name,
                "content": file_content,
            }
            self.page.evaluate(js_drop_script, payload)
            logger.info(f"JS-ін'єкція виконана успішно для {file_name}")
        except Exception as e:
            logger.error(f"Помилка в JS-evaluate: {str(e)}")
            raise

    # У класі UploadPage
    def upload_certificate(self, file_path):
        """Універсальний метод, який ми тепер використовуємо скрізь."""
        self.upload_via_drop(file_path)

    def return_to_main(self):
        """
        Натискає 'Back' для повернення, якщо панель ще відкрита.
        Додано перевірку видимості, щоб уникнути TimeoutError (скрін 05_05).
        """
        logger.info("Спроба повернутися до головного екрана...")

        # Перевіряємо, чи кнопка видима
        if self.back_button.is_visible():
            logger.info("Кнопка 'Back' видима, натискаю...")
            self.back_button.click()
        else:
            logger.info(
                "Кнопка 'Back' уже прихована (ng-hide). Схоже, панель закрилася автоматично."
            )
