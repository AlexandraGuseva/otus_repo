import time
import logging
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage
from pages.admin_login_page import AdminLoginPage
from pages.registration_page import RegistrationPage

logger = logging.getLogger(__name__)


class TestElements:

    @allure.feature("Главная страница")
    @allure.story("Проверка элементов")
    @allure.title("Проверка отображения элементов на главной странице")
    def test_main_page_elements(self, browser, base_url):
        logger.info("=== Запуск теста: test_main_page_elements ===")

        with allure.step("Открыть главную страницу"):
            page = MainPage(browser, base_url)
            page.open("/3-clothes")

        with allure.step("Проверить логотип"):
            assert page.is_logo_displayed(), "Логотип не отображается"
            logger.info("Логотип отображается")

        with allure.step("Проверить поле поиска"):
            assert page.is_search_input_displayed(), "Поле поиска не отображается"
            logger.info("Поле поиска отображается")

        with allure.step("Проверить кнопку корзины"):
            assert page.is_cart_button_displayed(), "Кнопка корзины не отображается"
            logger.info("Кнопка корзины отображается")

        with allure.step("Проверить главное меню"):
            assert page.is_main_menu_displayed(), "Главное меню не отображается"
            logger.info("Главное меню отображается")

        with allure.step("Проверить список товаров"):
            assert page.is_product_list_displayed(), "Список товаров не отображается"
            logger.info("Список товаров отображается")

    @allure.feature("Каталог")
    @allure.story("Проверка элементов")
    @allure.title("Проверка отображения элементов на странице каталога")
    def test_catalog_page_elements(self, browser, base_url):
        logger.info("=== Запуск теста: test_catalog_page_elements ===")

        with allure.step("Открыть страницу каталога"):
            page = CatalogPage(browser, base_url)
            page.open("/3-clothes")

        with allure.step("Проверить заголовок категории"):
            assert page.get_category_title() == "Clothes", "Неверный заголовок категории"
            logger.info("Заголовок категории верный")

        with allure.step("Проверить список товаров"):
            assert page.is_product_list_displayed(), "Список товаров не отображается"
            logger.info("Список товаров отображается")

        with allure.step("Проверить наличие товаров"):
            assert page.get_product_count() > 0, "Нет товаров в категории"
            logger.info(f"Количество товаров: {page.get_product_count()}")

    @allure.feature("Карточка товара")
    @allure.story("Проверка элементов")
    @allure.title("Проверка отображения элементов на карточке товара")
    def test_product_page_elements(self, browser, base_url):
        logger.info("=== Запуск теста: test_product_page_elements ===")

        main_page = MainPage(browser, base_url)

        with allure.step("Открыть главную страницу"):
            main_page.open("/")

        with allure.step("Получить название первого товара"):
            product_name = main_page.get_first_product_name()
            logger.info(f"Название товара: {product_name}")

        with allure.step("Кликнуть на первый товар"):
            main_page.click_first_product()

        with allure.step("Проверить название товара на странице"):
            time.sleep(3)
            page_text = browser.find_element(By.TAG_NAME, "body").text
            assert product_name.lower() in page_text.lower(), \
                f"Название '{product_name}' не найдено на странице"
            logger.info("Название товара найдено")

        with allure.step("Проверить наличие цены"):
            has_price = any(symbol in page_text for symbol in ['€', '$', '₽'])
            assert has_price, "Цена не найдена на странице"
            logger.info("Цена найдена")

        with allure.step("Проверить кнопку 'В корзину'"):
            add_to_cart_buttons = browser.find_elements(
                By.CSS_SELECTOR,
                "button[data-button-action='add-to-cart'], .add-to-cart, button[type='submit']"
            )
            assert len(add_to_cart_buttons) > 0, "Кнопка 'В корзину' не найдена"
            logger.info("Кнопка 'В корзину' найдена")

        @allure.feature("Админка")
        @allure.story("Проверка элементов")
        @allure.title("Проверка отображения элементов на странице входа в админку")
        def test_admin_login_page_elements(self, browser, base_url):
            logger.info("=== Запуск теста: test_admin_login_page_elements ===")

            with allure.step("Открыть страницу админки"):
                page = AdminLoginPage(browser, base_url)
                page.open("/admin-dev")

            with allure.step("Проверить логотип"):
                assert page.is_logo_displayed(), "Логотип админки не отображается"
                logger.info("Логотип админки отображается")

            with allure.step("Проверить поле email"):
                assert page.is_email_input_displayed(), "Поле email не отображается"
                logger.info("Поле email отображается")

            with allure.step("Проверить поле пароля"):
                assert page.is_password_input_displayed(), "Поле пароля не отображается"
                logger.info("Поле пароля отображается")

            with allure.step("Проверить кнопку входа"):
                assert page.is_login_button_displayed(), "Кнопка входа не отображается"
                logger.info("Кнопка входа отображается")

            with allure.step("Проверить ссылку 'Забыли пароль'"):
                assert page.is_forgot_password_link_displayed(), "Ссылка 'Забыли пароль' не отображается"
                logger.info("Ссылка 'Забыли пароль' отображается")

        @allure.feature("Регистрация")
        @allure.story("Проверка элементов")
        @allure.title("Проверка отображения элементов на странице регистрации")
        def test_registration_page_elements(self, browser, base_url):
            logger.info("=== Запуск теста: test_registration_page_elements ===")

            with allure.step("Открыть страницу регистрации"):
                page = RegistrationPage(browser, base_url)
                page.open("/registration")

            with allure.step("Проверить форму регистрации"):
                assert page.is_form_displayed(), "Форма регистрации не отображается"
                logger.info("Форма регистрации отображается")

            with allure.step("Проверить поле имени"):
                assert page.is_first_name_displayed(), "Поле имени не отображается"
                logger.info("Поле имени отображается")

            with allure.step("Проверить поле фамилии"):
                assert page.is_last_name_displayed(), "Поле фамилии не отображается"
                logger.info("Поле фамилии отображается")

            with allure.step("Проверить поле email"):
                assert page.is_email_displayed(), "Поле email не отображается"
                logger.info("Поле email отображается")

            with allure.step("Проверить поле пароля"):
                assert page.is_password_displayed(), "Поле пароля не отображается"
                logger.info("Поле пароля отображается")

            with allure.step("Проверить чекбокс согласия"):
                assert page.is_terms_displayed(), "Чекбокс согласия не отображается"
                logger.info("Чекбокс согласия отображается")