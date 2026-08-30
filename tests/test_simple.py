import pytest
from selenium.webdriver.common.by import By


class TestSimple:

    def test_open_page(self, browser, base_url):
            browser.get(base_url)
            assert "PrestaShop" in browser.title
            print("✅ Произошло чудо!!! Страница открыта.")


    def test_print_page_text(self, browser, base_url):
        browser.get(base_url + "/")

        import time
        time.sleep(5)

        body_text = browser.find_element(By.TAG_NAME, "body").text
        print("\n=== ВЕСЬ ТЕКСТ СТРАНИЦЫ ===")
        print(body_text[:1000])

        assert "€" in body_text or "$" in body_text or "₽" in body_text, "Валюта не найдена на странице"