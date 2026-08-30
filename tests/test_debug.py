import pytest
import time
import re
from selenium.webdriver.common.by import By


class TestDebug:

    def test_find_elements(self, browser, base_url):

        browser.get(base_url + "/")

        time.sleep(3)

        print("\n=== ПОИСК ЭЛЕМЕНТОВ НА СТРАНИЦЕ ===")
        print("URL:", browser.current_url)
        print("Title:", browser.title)

        selectors = [
            ("logo", "img.logo"),
            ("search", "input[name='s']"),
            ("cart", "div.cart-preview"),
            ("products", ".products"),
            ("price", ".price"),
        ]

        for name, selector in selectors:
            try:
                elements = browser.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✓ {name}: найдено {len(elements)} элементов")
                    if elements:
                        print(f"   Первый: {elements[0].tag_name} - {elements[0].text[:50]}")
                else:
                    print(f"✗ {name}: не найдено")
            except Exception as e:
                print(f"✗ {name}: ошибка - {e}")

        print("\n=== ПОИСК ЦЕНЫ ЧЕРЕЗ ТЕКСТ ===")
        body_text = browser.find_element(By.TAG_NAME, "body").text
        if "€" in body_text:
            print("✅ Цена найдена в тексте страницы!")
            prices = re.findall(r'[\d.,]+\s*[€]', body_text)
            print(f"Найдены цены: {prices}")
        else:
            print("❌ Цена не найдена в тексте")

        assert browser.title, "Заголовок не найден"