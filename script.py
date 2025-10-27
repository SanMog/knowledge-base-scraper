import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Домен сайта для создания полных ссылок
BASE_DOMAIN = "https://docs.cbooster.ru"
# URL главной страницы
START_URL = "https://docs.cbooster.ru/s/62cf5890-33fb-4f99-94ef-1622a6f6ae7a/doc/baza-znanij-credit-booster-IZoCJaGwZZ"

# Имя файла для сохранения
OUTPUT_FILE = "knowledge_base_content.txt"

# --- Настройка Selenium ---
service = Service()
options = webdriver.ChromeOptions()
# Раскомментируйте следующую строку, если не хотите, чтобы окно браузера открывалось
# options.add_argument('--headless')

try:
    driver = webdriver.Chrome(service=service, options=options)
    print("Браузер Chrome запущен.")
except Exception as e:
    print(f"Ошибка при запуске браузера: {e}")
    print(
        "Убедитесь, что chromedriver.exe находится в той же папке, что и скрипт, и его версия совпадает с версией вашего браузера Chrome.")
    exit()


def expand_all_nodes():
    """
    Находит и нажимает на все кнопки "Expand", чтобы раскрыть полное дерево оглавления.
    """
    print("Раскрываю все подпункты в оглавлении...")
    while True:
        try:
            # Ищем кнопки, которые еще не были раскрыты
            expand_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label="Expand"]')
            if not expand_buttons:
                print("Все подпункты раскрыты.")
                break  # Выходим из цикла, если кнопок "Expand" больше нет

            # Нажимаем на первую найденную кнопку
            button = expand_buttons[0]
            driver.execute_script("arguments[0].click();", button)  # Более надежный способ клика
            time.sleep(0.5)  # Даем время на подгрузку нового контента
        except Exception as e:
            print(f"Произошла ошибка при раскрытии узла: {e}")
            break


def get_all_page_links():
    """
    Собирает все ссылки из ПОЛНОСТЬЮ раскрытого оглавления.
    """
    print("Загружаю главную страницу...")
    driver.get(START_URL)
    links = {}
    try:
        # Ждем, пока загрузится само оглавление
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.sc-tyaw0p-3"))
        )

        # *** НОВЫЙ ШАГ: Раскрываем все узлы перед сбором ссылок ***
        expand_all_nodes()

        print("Собираю финальный список ссылок...")
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        nav_links = soup.find_all('a', class_='sc-tyaw0p-3')

        for link in nav_links:
            href = link.get('href')
            title = link.get_text(strip=True)
            if href and title and not href.startswith('#'):
                links[href] = title

        print(f"Найдено {len(links)} уникальных ссылок.")
        return links

    except Exception as e:
        print(f"Не удалось загрузить оглавление или найти ссылки: {e}")
        return None


def get_page_content(url):
    """
    Извлекает контент с отдельной страницы.
    """
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ProseMirror"))
        )
        content_div = driver.find_element(By.CSS_SELECTOR, "div.ProseMirror")
        return content_div.text
    except Exception as e:
        error_message = f"    -> Не удалось загрузить контент. Ошибка: {str(e).splitlines()[0]}"
        print(error_message)
        return error_message


def main():
    page_links = get_all_page_links()

    if not page_links:
        print("Не удалось получить ссылки. Завершение работы.")
        driver.quit()
        return

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        print(f"Начинаю сбор данных. Результат будет сохранен в: {OUTPUT_FILE}")

        i = 1
        total = len(page_links)
        for relative_url, title in page_links.items():
            full_url = BASE_DOMAIN + relative_url

            print(f"[{i}/{total}] Обрабатываю: {title}")

            f.write("=" * 80 + "\n")
            f.write(f"СТРАНИЦА: {title}\n")
            f.write(f"URL: {full_url}\n")
            f.write("=" * 80 + "\n\n")

            content = get_page_content(full_url)
            f.write(content)
            f.write("\n\n\n")

            # Увеличиваем паузу, чтобы снизить риск блокировки
            time.sleep(1)
            i += 1

    print("Сбор данных успешно завершен!")
    driver.quit()


if __name__ == "__main__":
    main()