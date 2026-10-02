import logging
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.catalog_page import CatalogPage
from pages.admin_login_page import AdminLoginPage
from pages.product_page import ProductPage

logger = logging.getLogger(__name__)


class TestScenarios:

    @allure.feature("Админка")
    @allure.story("Логин и выход")
    @allure.title("Логин-разлогин в админку")
    def test_admin_login_logout(self, browser, base_url):
        """логин-разлогин админки"""
        logger.info("=== Запуск теста: test_admin_login_logout ===")

        with allure.step("Открыть страницу админки"):
            admin_page = AdminLoginPage(browser, base_url)
            admin_page.open_admin_page()

        with allure.step("Ввести email и пароль"):
            admin_page.enter_email("admin@example.com")
            admin_page.enter_password("Admin123!")
            admin_page.click_login_in()
            admin_page.assert_administration_logged_in()

        with allure.step("Выйти из админки"):
            browser.get(base_url + "/admin-dev/logout")

        with allure.step("Проверить возврат на страницу логина"):
            WebDriverWait(browser, 10).until(
                lambda d: "login" in d.current_url.lower()
            )
            assert "login" in browser.current_url.lower()

    @allure.feature("Корзина")
    @allure.story("Добавление товара")
    @allure.title("Добавление случайного товара с главной страницы в корзину")
    def test_add_random_product_to_cart(self, browser, base_url):
        """случайный товар с главной страницы в корзину"""
        logger.info("=== Запуск теста: test_add_random_product_to_cart ===")

        main_page = MainPage(browser, base_url)

        with allure.step("Открыть главную страницу"):
            main_page.open("/")

        with allure.step("Получить название первого товара"):
            product_name = main_page.get_first_product_name()

        with allure.step("Добавить товар в корзину"):
            main_page.add_first_product_to_cart()

        with allure.step("Открыть корзину"):
            main_page.click(MainPage.CART_BUTTON)
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

        with allure.step("Проверить, что товар есть в корзине"):
            cart_text = browser.find_element(By.TAG_NAME, "body").text
            assert product_name in cart_text, f"Товар '{product_name}' не найден в корзине"

    @allure.feature("Валюта")
    @allure.story("Переключение валюты на главной")
    @allure.title("Проверка смены цен при переключении валюты на главной")
    def test_currency_change_on_main_page(self, browser, base_url):
        """проверка, что при переключении валют цены меняются на главной"""
        logger.info("=== Запуск теста: test_currency_change_on_main_page ===")

        main_page = MainPage(browser, base_url)

        with allure.step("Открыть главную страницу"):
            main_page.open("/")

        with allure.step("Определить текущую валюту и цену"):
            current_currency = main_page.get_current_currency()
            price_before = main_page.get_first_product_price()
            logger.info(f"Текущая валюта: {current_currency}, цена: {price_before}")

        with allure.step("Переключиться на другую валюту"):
            new_currency = "$" if "€" in current_currency else "€"
            main_page.switch_currency(new_currency)
            logger.info(f"Переключение с {current_currency} на {new_currency}")

        with allure.step("Проверить, что цена изменилась"):
            price_after = main_page.get_first_product_price()
            logger.info(f"Цена после переключения: {price_after}")
            assert price_before != price_after, \
                f"Цена не изменилась при переключении с {current_currency} на {new_currency}"

            @allure.feature("Валюта")
            @allure.story("Переключение валюты в каталоге")
            @allure.title("Проверка смены цен при переключении валюты в каталоге")
            def test_currency_change_on_catalog_page(self, browser, base_url):
                """проверка, что при переключении валют цены меняются в каталоге"""
                logger.info("=== Запуск теста: test_currency_change_on_catalog_page ===")

                catalog_page = CatalogPage(browser, base_url)
                main_page = MainPage(browser, base_url)

                with allure.step("Открыть каталог"):
                    catalog_page.open("/3-clothes")

                with allure.step("Получить цену до переключения"):
                    price_before = catalog_page.get_first_product_price()
                    logger.info(f"Цена до переключения: {price_before}")

                with allure.step("Определить текущую валюту через главную"):
                    main_page.open("/")
                    current_currency = main_page.get_current_currency()
                    logger.info(f"Текущая валюта: {current_currency}")

                with allure.step("Переключиться на другую валюту"):
                    new_currency = "$" if "€" in current_currency else "€"
                    main_page.switch_currency(new_currency)
                    logger.info(f"Переключение с {current_currency} на {new_currency}")

                with allure.step("Снова открыть каталог"):
                    catalog_page.open("/3-clothes")

                with allure.step("Проверить, что цена изменилась"):
                    price_after = catalog_page.get_first_product_price()
                    logger.info(f"Цена после переключения: {price_after}")
                    assert price_before != price_after, \
                        f"Цена не изменилась при переключении с {current_currency} на {new_currency}"