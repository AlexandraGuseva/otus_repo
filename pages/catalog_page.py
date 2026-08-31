from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re


class CatalogPage(BasePage):
    """Страница каталога PrestaShop"""

    CATEGORY_TITLE = (By.CSS_SELECTOR, "#js-product-list-header > div > h1")
    PRODUCT_LIST = (By.CSS_SELECTOR, ".products")
    PRODUCTS = (By.CSS_SELECTOR, ".product-miniature")
    FIRST_PRODUCT = (By.CSS_SELECTOR, ".product-miniature:first-child")
    FIRST_PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-miniature:first-child .product-miniature__price")
    PAGINATION = (By.CSS_SELECTOR, "nav.pagination")

    def open(self, url=""):
        super().open(url)
        return self

    def get_category_title(self):
        return self.get_text(self.CATEGORY_TITLE)

    def is_product_list_displayed(self):
        return self.is_displayed(self.PRODUCT_LIST)

    def find_elements(self, locator, timeout=10):
        """Возвращает список элементов (с ожиданием появления хотя бы одного)."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located(locator)
            )
        except TimeoutException:
            return []

    def get_product_count(self):
        """Возвращает количество товаров в каталоге."""
        products = self.find_elements(self.PRODUCTS)
        return len(products)

    def is_pagination_displayed(self):
        try:
            return self.is_displayed(self.PAGINATION)
        except TimeoutException:
            return False

    def get_first_product_price(self):
        price_text = self.get_text(self.FIRST_PRODUCT_PRICE)
        price_match = re.search(r'[\d.,]+', price_text)
        if price_match:
            return float(price_match.group().replace(',', '.'))
        return 0.0