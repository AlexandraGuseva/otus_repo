import logging
import re
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class ProductPage(BasePage):
    """Страница карточки товара"""

    PRODUCT_PRICE = (By.CSS_SELECTOR, ".current-price .price, .product-price, .price")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, "div.product-description")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[data-button-action='add-to-cart']")

    def get_product_name(self):
        """Возвращает название товара из заголовка страницы или H1"""
        try:
            name = self.get_text((By.CSS_SELECTOR, "h1, .product-title, .product-name, .h1"))
            logger.info(f"Название товара (из H1): {name}")
            return name
        except Exception:
            title = self.driver.title
            if "PrestaShop" in title:
                title = title.replace("PrestaShop", "").strip()
            if "|" in title:
                title = title.split("|")[0].strip()
            logger.info(f"Название товара (из title): {title}")
            return title

    def get_product_price(self):
        price_text = self.get_text(self.PRODUCT_PRICE)
        price_match = re.search(r'[\d.,]+', price_text)
        if price_match:
            price = float(price_match.group().replace(',', '.'))
            logger.info(f"Цена товара на карточке: {price}")
            return price
        logger.warning("Цена товара не найдена на карточке")
        return 0.0

    def is_description_displayed(self):
        return self.is_displayed(self.PRODUCT_DESCRIPTION)

    def is_add_to_cart_button_displayed(self):
        return self.is_displayed(self.ADD_TO_CART_BUTTON)