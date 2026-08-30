from pages.main_page import MainPage
from pages.catalog_page import CatalogPage
from pages.admin_login_page import AdminLoginPage
from pages.product_page import ProductPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestScenarios:

    def test_admin_login_logout(self, browser, base_url):
        """логин-разлогин админки"""
        admin_page = AdminLoginPage(browser, base_url)
        admin_page.open_admin_page()
        admin_page.enter_email("admin@example.com")
        admin_page.enter_password("Admin123!")
        admin_page.click_login_in()
        admin_page.assert_administration_logged_in()

        browser.get(base_url + "/admin-dev/logout")

        WebDriverWait(browser, 10).until(
            lambda d: "login" in d.current_url.lower()
        )
        assert "login" in browser.current_url.lower()

    def test_add_random_product_to_cart(self, browser, base_url):
        """случайный товар с главной страницы в корзину"""
        main_page = MainPage(browser, base_url)
        main_page.open("/")

        product_name = main_page.get_first_product_name()

        main_page.add_first_product_to_cart()

        main_page.click(MainPage.CART_BUTTON)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        cart_text = browser.find_element(By.TAG_NAME, "body").text
        print(f"🔍 Текст корзины: {cart_text[:500]}")

        assert product_name in cart_text, f"Товар '{product_name}' не найден в корзине"

        print(f"✅ Товар '{product_name}' успешно добавлен в корзину!")

    def test_currency_change_on_main_page(self, browser, base_url):
        """проверка, что при переключении валют цены на товары меняются на главной"""
        main_page = MainPage(browser, base_url)
        main_page.open("/")

        price_eur = main_page.get_first_product_price()

        main_page.switch_currency("$")

        price_usd = main_page.get_first_product_price()

        assert price_eur != price_usd, "Цена не изменилась при переключении валюты"

        main_page.switch_currency("€")
        price_eur_again = main_page.get_first_product_price()

        assert abs(price_eur - price_eur_again) < 0.01, "Цена не вернулась к исходной"

    def test_currency_change_on_catalog_page(self, browser, base_url):
        """проверка, что при переключении валют цены на товары меняются в каталоге"""
        catalog_page = CatalogPage(browser, base_url)
        catalog_page.open("/3-clothes")

        price_usd = catalog_page.get_first_product_price()

        main_page = MainPage(browser, base_url)
        main_page.open("/")
        main_page.switch_currency("€")

        catalog_page.open("/3-clothes")