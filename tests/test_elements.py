import pytest
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage
from pages.admin_login_page import AdminLoginPage
from pages.registration_page import RegistrationPage


class TestElements:

    def test_main_page_elements(self, browser, base_url):
        page = MainPage(browser, base_url)
        page.open("/3-clothes")

        assert page.is_logo_displayed(), "Логотип не отображается"
        assert page.is_search_input_displayed(), "Поле поиска не отображается"
        assert page.is_cart_button_displayed(), "Кнопка корзины не отображается"
        assert page.is_main_menu_displayed(), "Главное меню не отображается"
        assert page.is_product_list_displayed(), "Список товаров не отображается"

    def test_catalog_page_elements(self, browser, base_url):
        """проверка товаров в каталоге"""
        page = CatalogPage(browser, base_url)
        page.open("/3-clothes")

        assert page.get_category_title() == "Clothes", "Неверный заголовок категории"
        assert page.is_product_list_displayed(), "Список товаров не отображается"
        assert page.get_product_count() > 0, "Нет товаров в категории"

    def test_product_page_elements(self, browser, base_url):
        """Проверка элементов на карточке товара"""

        main_page = MainPage(browser, base_url)
        main_page.open("/")

        product_name = main_page.get_first_product_name()

        main_page.click_first_product()

        time.sleep(3)

        page_text = browser.find_element(By.TAG_NAME, "body").text

        assert product_name.lower() in page_text.lower(), f"Название '{product_name}' не найдено на странице"

        has_price = any(symbol in page_text for symbol in ['€', '$', '₽'])
        assert has_price, "Цена не найдена на странице"

        add_to_cart_buttons = browser.find_elements(By.CSS_SELECTOR,
                                                    "button[data-button-action='add-to-cart'], .add-to-cart, button[type='submit']")
        assert len(add_to_cart_buttons) > 0, "Кнопка 'В корзину' не найдена"

    def test_admin_login_page_elements(self, browser, base_url):
        """проверка админки"""
        page = AdminLoginPage(browser, base_url)
        page.open("/admin-dev")

        assert page.is_logo_displayed(), "Логотип админки не отображается"
        assert page.is_email_input_displayed(), "Поле email не отображается"
        assert page.is_password_input_displayed(), "Поле пароля не отображается"
        assert page.is_login_button_displayed(), "Кнопка входа не отображается"
        assert page.is_forgot_password_link_displayed(), "Ссылка 'Забыли пароль' не отображается"

    def test_registration_page_elements(self, browser, base_url):
        """проверка формы регистрации"""
        page = RegistrationPage(browser, base_url)
        page.open("/registration")

        assert page.is_form_displayed(), "Форма регистрации не отображается"
        assert page.is_first_name_displayed(), "Поле имени не отображается"
        assert page.is_last_name_displayed(), "Поле фамилии не отображается"
        assert page.is_email_displayed(), "Поле email не отображается"
        assert page.is_password_displayed(), "Поле пароля не отображается"
        assert page.is_terms_displayed(), "Чекбокс согласия не отображается"