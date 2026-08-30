from selenium.webdriver.common.by import By
from pages.base_page import BasePage
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
        self.switch_to_iframe()
        return self

    def get_category_title(self):
        return self.get_text(self.CATEGORY_TITLE)

    def is_product_list_displayed(self):
        return self.find_element(self.PRODUCT_LIST).is_displayed()

    def get_product_count(self):
        return len(self.find_elements(self.PRODUCTS))

    def is_pagination_displayed(self):
        try:
            return self.find_element(self.PAGINATION).is_displayed()
        except:
            return False

    def get_first_product_price(self):
        price_text = self.get_text(self.FIRST_PRODUCT_PRICE)
        price_match = re.search(r'[\d.,]+', price_text)
        if price_match:
            return float(price_match.group().replace(',', '.'))
        return 0.0