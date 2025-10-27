# Парсер Базы Знаний "Outline"

Этот скрипт на Python использует Selenium для автоматического сбора всех статей из онлайн-базы знаний и сохранения их в один текстовый файл.

## Основные возможности

-   Автоматически раскрывает все разделы и подразделы в навигационном меню.
-   Собирает полный список ссылок на все уникальные страницы.
-   Последовательно обходит каждую страницу, извлекает её текстовое содержимое.
-   Сохраняет результат в файл `knowledge_base_content.txt`, форматируя его для удобной читаемости.

## Требования

-   Python 3.8+
-   Google Chrome
-   ChromeDriver

## Установка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/SanMog/knowledge-base-scraper.git
    cd knowledge-base-scraper
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Установите зависимости:**
    ```bash
    pip install selenium beautifulsoup4
    ```

4.  **Скачайте ChromeDriver** с [официального сайта](https://googlechromelabs.github.io/chrome-for-testing/) и поместите `chromedriver.exe` в папку с проектом. Версия должна совпадать с версией вашего браузера Chrome.

5.  **Запустите скрипт:**
    ```bash
    python script.py
    ```