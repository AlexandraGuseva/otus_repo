import logging
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class MainPage(BasePage):
    """Главная страница PrestaShop"""

    LOGO = (By.CSS_SELECTOR, "img[alt='Logo'], img[alt='PrestaShop'], .logo img, #header img")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='s'], #search-input, .search-input")
    CART_BUTTON = (By.CSS_SELECTOR, ".cart-preview, .cart-link, #_desktop_cart")
    MAIN_MENU = (By.CSS_SELECTOR, ".top-menu, .menu, .ps-mainmenu")

    PRODUCT_LIST = (By.CSS_SELECTOR, "#js-product-list > div.products")
    FIRST_PRODUCT = (By.CSS_SELECTOR,
                     "#content > section.ps-featuredproducts > div > div.module-products__list > div > article:nth-child(1)")
    FIRST_PRODUCT_NAME = (By.CSS_SELECTOR,
                          "#content > section.ps-featuredproducts > div > div.module-products__list > div > article:nth-child(1) > div > div.product-miniature__bottom > div.product-miniature__infos > a")
    FIRST_PRODUCT_PRICE = (By.CSS_SELECTOR,
                           "#content > section.ps-featuredproducts > div > div.module-products__list > div > article:nth-child(1) > div > div.product-miniature__bottom > div.product-miniature__infos > div.product-miniature__prices > div.product-miniature__price")

    CURRENCY_DROPDOWN = (By.CSS_SELECTOR, "#_desktop_ps_currencyselector > div > select")
    CURRENCY_OPTIONS = (By.CSS_SELECTOR, "#_desktop_ps_currencyselector > div > select option")

    def open(self, url=""):
        logger.info(f"Открытие главной страницы: {url}")
        super().open(url)
        return self

    def is_logo_displayed(self):
        logger.info("Проверка отображения логотипа")
        return self.wait_for_element(self.LOGO).is_displayed()

    def is_search_input_displayed(self):
        logger.info("Проверка отображения поля поиска")
        return self.wait_for_element(self.SEARCH_INPUT).is_displayed()

    def is_cart_button_displayed(self):
        logger.info("Проверка отображения кнопки корзины")
        return self.wait_for_element(self.CART_BUTTON).is_displayed()

    def is_main_menu_displayed(self):
        logger.info("Проверка отображения главного меню")
        return self.wait_for_element(self.MAIN_MENU).is_displayed()

    def is_product_list_displayed(self):
        logger.info("Проверка отображения списка товаров")
        return self.wait_for_element(self.PRODUCT_LIST).is_displayed()

    def get_first_product_name(self):
        logger.info("Получение названия первого товара")
        name = self.get_text(self.FIRST_PRODUCT_NAME)
        logger.info(f"Название товара: {name}")
        return name

    def get_first_product_price(self):
        logger.info("Получение цены первого товара")
        price_text = self.get_text(self.FIRST_PRODUCT_PRICE)
        price_match = re.search(r'[\d.,]+', price_text)
        if price_match:
            price = float(price_match.group().replace(',', '.'))
            logger.info(f"Цена товара: {price}")
            return price
        logger.warning("Цена не найдена")
        return 0.0

    def click_first_product(self):
        logger.info("Клик по первому товару")
        product_link = self.wait_for_element(self.FIRST_PRODUCT_NAME)
        self.driver.execute_script("arguments[0].click();", product_link)
        logger.info("Клик выполнен")
        return self

    def add_first_product_to_cart(self):
        logger.info("Добавление первого товара в корзину")

        product = self.wait_for_element(self.FIRST_PRODUCT)
        actions = ActionChains(self.driver)
        actions.move_to_element(product).perform()
        logger.info("Наведение на товар выполнено")

        add_button = self.wait_for_element(
            (By.CSS_SELECTOR, ".product-miniature:first-child button[data-button-action='add-to-cart']"))

        try:
            add_button.click()
            logger.info("Клик по кнопке 'В корзину' выполнен стандартно")
        except Exception:
            self.driver.execute_script("arguments[0].click();", add_button)
            logger.info("Клик по кнопке 'В корзину' выполнен через JavaScript")

        close_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#blockcart-modal > div > div > div.modal-header > button"))
        )
        close_button.click()
        logger.info("Модальное окно закрыто")

        return self

    def switch_currency(self, currency_symbol):
        logger.info(f"Переключение валюты на {currency_symbol}")

        select_element = self.wait_for_element(self.CURRENCY_DROPDOWN)
        select = Select(select_element)

        for option in select.options:
            if currency_symbol in option.text:
                select.select_by_visible_text(option.text)
                logger.info(f"Валюта переключена на {currency_symbol}")
                time.sleep(1)
                return self

        error_msg = f"Валюта {currency_symbol} не найдена"
        logger.error(error_msg)
        raise ValueError(error_msg)

    def get_current_currency(self):
        """Возвращает текущую валюту (например, '€' или '$')"""
        logger.info("Определение текущей валюты")
        select_element = self.wait_for_element(self.CURRENCY_DROPDOWN)
        select = Select(select_element)
        current = select.first_selected_option.text
        logger.info(f"Текущая валюта: {current}")
        return current