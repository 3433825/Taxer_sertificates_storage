# 🛡️ Taxer Certificate Storage QA Automation

[![Playwright Tests](https://github.com/3433825/Taxer_sertificates_storage/actions/workflows/playwright_tests.yml/badge.svg)](https://github.com/3433825/Taxer_sertificates_storage/actions)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Managed by uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

Проєкт з автоматизації тестування сервісу управління сертифікатами. Фреймворк побудований на базі **Playwright** та **Pytest** з використанням сучасного менеджеру пакетів **uv** та налаштованим **CI/CD** через GitHub Actions.

## 🚀 Технологічний стек
* **Мова:** Python 3.12+
* **Тестовий фреймворк:** Pytest
* **Інструмент автоматизації:** Playwright (Page Object Model)
* **Пакетний менеджер:** [uv](https://docs.astral.sh/uv/) (швидка інсталяція та керування залежностями)
* **CI/CD:** GitHub Actions (автоматичний запуск тестів при кожному push)
* **Логування:** Python `logging` (збереження артефактів виконання)
* **Репортинг:** [Allure Report](https://allurereport.org/) (інтерактивні HTML-звіти з історією запусків)

---

## 🛠️ Архітектура проекту
Проєкт реалізовано за паттерном **Page Object Model (POM)** для забезпечення чистоти коду та легкої підтримки:

* `pages/` — класи з описом сторінок та методів взаємодії.
* `tests/` — набори тестів (E2E, UI Indicators, Interactions).
* `utils/` — допоміжні інструменти (логер, константи).
* `data/` — тестові артефакти (валідні та прострочені сертифікати).
* `docs/` — тестова документація
* `allure-results/` — директорія з результатами запусків для Allure (генерується автоматично).
* `.github/workflows/` — конфігурація автоматичного запуску тестів у хмарі.

---

## Тестове завдання на вакансію General QA Engineer

Тестове завдання на вакансію тестувальника пов'язане із тестовим завданням для розробників. Необхідно провести тестування веб-сторінки, перевірити відповідність ТЗ, знайти та описати помилки. Підсумком має стати документ, який може бути передано розробникам для виправлення знайдених проблем. Жодного жорсткого формату цього документа не буде задаватися, але звіт повинен містити достатньо інформації для розробників, щоб повторити та усунути проблеми. Приймаються не тільки помилки, а й побажання щодо юзабіліті або юзер-експірієнсу. Пишіть про все, що можна покращити.

Підказки: у запропонованому рішенні навмисно зроблено кілька помилок. Не варто розуміти помилку, як тільки те, що не працює. Увага потрібно приділити всім аспектам сторінки.

Завдання на автоматизацію:
Необхідно автоматизувати E2E сценарій в якому буде відкрито сторінку, завантажено сертифікат, перевірено дані сертифікату у списку сертифікатів та в таблиці з деталями про сертифікат.

Відсутні обмеження на мови програмування та бібліотеки для автоматизації, але плюсом буде використання TS+Playwright.

## Тестове завдання на вакансію Web-розробник

Суть завдання: реалізувати на JavaScript сховище сертифікатів у браузері.
Зовні це має бути сторінка, де є табличка поточних сертифікатів що вже додані.
Клацнувши на сертифікат, можна отримати коротку інформацію з нього. Додані
сертифікати зберігаються в LocalStorage, тобто під час перезавантаження сторінки повинні відображатися вже додані сертифікати. Додати сертифікат у сховище
можна, перетягнувши файл у поле drag&drop'а.


## 🔍 Покриття тестами та знайдені дефекти
В ході автоматизації було виявлено ряд критичних зауважень (BUG), які задокументовані безпосередньо в тестах:

| ID Тесту | Опис перевірки | Статус | Коментар |
| :--- | :--- | :--- | :--- |
| **TC-05** | Завантаження валідного сертифікату | ✅ Pass | Успішне додавання у список |
| **BUG-01** | Текст головної кнопки | ❌ Fail | Кнопка має текст "Завантажити" замість "Додати" |
| **BUG-08** | Порядок полів у деталях | ❌ Fail | Порядок полів не відповідає ТЗ |
| **BUG-11** | Активний індикатор | ❌ Fail | Відсутній символ `►` біля вибраного сертифікату |
| **E2E Flow** | Повний цикл роботи з сертифікатом | ✅ Pass | Від завантаження до перевірки деталей |

---

## 💻 Локальний запуск

### 1. Встановлення залежностей (через uv)
Якщо у вас встановлено `uv`:
```bash
uv sync
```

### 2. Встановлення браузерів Playwright
```bash
uv run playwright install --with-deps chromium
```

### 3. Запуск тестів
```bash
# У фоновому режимі (headless)
uv run pytest

# З відкритим браузером та уповільненням
uv run pytest --headed --slowmo 500
```

---

## 📊 Allure Reports

[Allure Report](https://allurereport.org/) — інтерактивний HTML-звіт із деталями кожного тесту, скріншотами, кроками виконання та історією запусків.

### Встановлення

#### 1. Додати залежність `allure-pytest`
```bash
uv add --dev allure-pytest
```

#### 2. Встановити Allure CLI

Allure CLI потребує **Java 8+**. Встановіть відповідно до вашої ОС:

**macOS (Homebrew):**
```bash
brew install allure
```

**Windows (Scoop):**
```bash
scoop install allure
```

**Linux (вручну):**
```bash
curl -o allure.tgz -L https://github.com/allure-framework/allure2/releases/latest/download/allure-commandline-tgz.tar.gz
tar -xzf allure.tgz
sudo mv allure-*/bin/allure /usr/local/bin/allure
```

Перевірка встановлення:
```bash
allure --version
```

---

### Запуск тестів із генерацією результатів

```bash
uv run pytest --alluredir=allure-results
```

Результати зберігаються у директорію `allure-results/`. При повторних запусках нові результати **додаються** до існуючих — це дозволяє зберігати історію.

---

### Перегляд звіту локально

```bash
# Відкрити звіт у браузері (запускає локальний сервер)
allure serve allure-results

# Або: згенерувати статичний HTML у директорію allure-report/
allure generate allure-results -o allure-report --clean
allure open allure-report
```

> **`--clean`** — очищає попередній звіт перед генерацією нового.

---

### Запуск із додатковими параметрами

```bash
# З відкритим браузером та збереженням результатів для Allure
uv run pytest --headed --slowmo 500 --alluredir=allure-results

# Тільки певна група тестів
uv run pytest tests/e2e/ --alluredir=allure-results
```

---

### Налаштування `pytest.ini`

Щоб не вказувати `--alluredir` щоразу вручну, додайте до `pytest.ini`:

```ini
[pytest]
addopts = --alluredir=allure-results
```

---

## ☁️ CI/CD (GitHub Actions)

Тести автоматично запускаються в Docker-контейнері при кожному оновленні коду.

* **Швидкість:** Завдяки використанню `uv`, час підготовки оточення скорочено на ~70%.
* **Артефакти:** Після кожного запуску в Actions доступні лог-файли та Allure-результати для детального аналізу.

### Приклад workflow з Allure

```yaml
name: Playwright Tests (UV) with Allure

on:
  # Запускаємо Лінтер при кожному пуші в будь-яку гілку (включаючи fix-ci-pipeline)
  # Але важкі тести запустимо тільки за умов нижче
  push:
    branches: [ main, master, fix-ci-pipeline ]
  
  pull_request:
    branches: [ main, master ]
    
  workflow_dispatch:

permissions:
  contents: write

jobs:
  # НОВА ШВИДКА JOB ДЛЯ ПЕРЕВІРКИ КОДУ
  lint:
    name: Code Quality (Linter)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v5
      - name: Run Ruff Check
        # Ruff перевірить синтаксис за 1-2 секунди
        run: uv run ruff check .

  # ОСНОВНА JOB З ТЕСТАМИ
  test:
    name: Run Pytest & Allure
    runs-on: ubuntu-latest
    # Ця job запуститься ТІЛЬКИ якщо:
    # 1. Це Pull Request у main/master
    # 2. Це Push у main/master
    # 3. АБО якщо запуск вручну (workflow_dispatch)
    if: |
      github.event_name == 'pull_request' || 
      (github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master')) ||
      github.event_name == 'workflow_dispatch'
    
    needs: lint # Тести почнуться тільки якщо Лінтер пройшов успішно
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true

      - name: Set up Python
        run: uv python install 3.12

      - name: Install dependencies
        run: uv sync --frozen

      - name: Install Playwright Browsers
        run: uv run playwright install --with-deps chromium

      - name: Run Tests
        env:
          BASE_URL: ${{ secrets.BASE_URL }}
          CERT_VALID: "data/valid_cert.cer"
          CERT_EXPIRED: "data/expired.cer"
        run: |
          mkdir -p logs
          PYTHONPATH=. uv run pytest . -v -s --log-cli-level=INFO --alluredir=allure-results

      - name: Upload Logs & Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: execution-artifacts
          path: |
            logs/
            allure-results/

      # Далі йдуть кроки Checkout gh-pages, Generate Allure та Publish (як у попередньому варіанті)
      - name: Checkout gh-pages
        uses: actions/checkout@v4
        if: always()
        continue-on-error: true
        with:
          ref: gh-pages
          path: gh-pages-dir

      - name: Generate Allure report
        uses: andgineer/allure-report@v3.6
        id: allure-report
        if: always()
        with:
          allure-results: allure-results
          website: gh-pages-dir
          reports-site-path: builds/tests

      - name: Publish Allure report to GitHub Pages
        if: ${{ always() && (steps.allure-report.outcome == 'success') }}
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_branch: gh-pages
          publish_dir: ${{ steps.allure-report.outputs.reports-site }}
          destination_dir: ${{ steps.allure-report.outputs.reports-site-path }}
```

> Звіт публікується на **GitHub Pages** після кожного запуску та зберігає **повну історію** всіх запусків.
> Для активації GitHub Pages: `Settings → Pages → Branch: gh-pages → /(root)`.

---

### 👨‍💻 Автор
**Олексій Шаповалов** — QA Automation Engineer (Python)
*Досвід у створенні масштабованих фреймворків та інтеграції їх у CI/CD процеси.*

---