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
        logger.info("Получение названия товара")
        try:
            name = self.get_text((By.CSS_SELECTOR, "h1, .product-title, .product-name, .h1"))
            logger.info(f"Название товара найдено: {name}")
            return name
        except Exception:
            logger.info("Название не найдено через селекторы, пробуем взять из заголовка страницы")
            title = self.driver.title
            if "PrestaShop" in title:
                title = title.replace("PrestaShop", "").strip()
            if "|" in title:
                title = title.split("|")[0].strip()
            logger.info(f"Название из заголовка: {title}")
            return title

    def get_product_price(self):
        logger.info("Получение цены товара")
        price_text = self.get_text(self.PRODUCT_PRICE)
        price_match = re.search(r'[\d.,]+', price_text)
        if price_match:
            price = float(price_match.group().replace(',', '.'))
            logger.info(f"Цена товара: {price}")
            return price
        logger.warning("Цена не найдена")
        return 0.0

    def is_description_displayed(self):
        logger.info("Проверка отображения описания товара")
        return self.is_displayed(self.PRODUCT_DESCRIPTION)

    def is_add_to_cart_button_displayed(self):
        logger.info("Проверка отображения кнопки 'В корзину'")
        return self.is_displayed(self.ADD_TO_CART_BUTTON)