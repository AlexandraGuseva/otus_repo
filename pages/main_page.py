from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import re


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
        super().open(url)
        return self

    def is_logo_displayed(self):
        return self.find_element(self.LOGO).is_displayed()

    def is_search_input_displayed(self):
        return self.find_element(self.SEARCH_INPUT).is_displayed()

    def is_cart_button_displayed(self):
        return self.find_element(self.CART_BUTTON).is_displayed()

    def is_main_menu_displayed(self):
        return self.find_element(self.MAIN_MENU).is_displayed()

    def is_product_list_displayed(self):
        return self.find_element(self.PRODUCT_LIST).is_displayed()

    def get_first_product_name(self):
        return self.get_text(self.FIRST_PRODUCT_NAME)

    def get_first_product_price(self):
        price_text = self.get_text(self.FIRST_PRODUCT_PRICE)
        price_match = re.search(r'[\d.,]+', price_text)
        if price_match:
            return float(price_match.group().replace(',', '.'))
        return 0.0

    def add_first_product_to_cart(self):
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        product = self.find_element(self.FIRST_PRODUCT)
        actions = ActionChains(self.driver)
        actions.move_to_element(product).perform()

        add_button = self.find_element(
            (By.CSS_SELECTOR, ".product-miniature:first-child button[data-button-action='add-to-cart']"))
        self.driver.execute_script("arguments[0].click();", add_button)

        close_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#blockcart-modal > div > div > div.modal-header > button"))
        )
        close_button.click()

        return self

    def switch_currency(self, currency_symbol):
        """Переключает валюту через выпадающий список <select>"""
        from selenium.webdriver.support.ui import Select
        import time

        select_element = self.wait_for_element((By.CSS_SELECTOR, "#_desktop_ps_currencyselector > div > select"))
        select = Select(select_element)

        for option in select.options:
            if currency_symbol in option.text:
                select.select_by_visible_text(option.text)
                time.sleep(2)
                return self

        raise ValueError(f"Валюта {currency_symbol} не найдена в выпадающем списке")