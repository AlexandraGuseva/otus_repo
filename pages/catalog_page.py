import logging
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CatalogPage(BasePage):
    """Страница каталога PrestaShop"""

    CATEGORY_TITLE = (By.CSS_SELECTOR, "#js-product-list-header > div > h1")
    PRODUCT_LIST = (By.CSS_SELECTOR, ".products")
    PRODUCTS = (By.CSS_SELECTOR, ".product-miniature")
    FIRST_PRODUCT = (By.CSS_SELECTOR, ".product-miniature:first-child")
    FIRST_PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-miniature:first-child .product-miniature__price")
    PAGINATION = (By.CSS_SELECTOR, "nav.pagination")

    def open(self, url=""):
        logger.info(f"Открытие страницы каталога: {url}")
        super().open(url)
        return self

    def get_category_title(self):
        logger.info("Получение заголовка категории")
        title = self.get_text(self.CATEGORY_TITLE)
        logger.info(f"Заголовок категории: {title}")
        return title

    def is_product_list_displayed(self):
        logger.info("Проверка отображения списка товаров")
        return self.is_displayed(self.PRODUCT_LIST)

    def find_elements(self, locator, timeout=10):
        logger.info(f"Поиск элементов: {locator}")
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located(locator)
            )
            logger.info(f"Найдено элементов: {len(elements)}")
            return elements
        except TimeoutException:
            logger.warning(f"Элементы не найдены за {timeout} секунд: {locator}")
            return []

    def get_product_count(self):
        logger.info("Подсчёт количества товаров")
        products = self.find_elements(self.PRODUCTS)
        count = len(products)
        logger.info(f"Количество товаров: {count}")
        return count

    def is_pagination_displayed(self):
        logger.info("Проверка отображения пагинации")
        try:
            result = self.is_displayed(self.PAGINATION)
            logger.info(f"Пагинация отображается: {result}")
            return result
        except TimeoutException:
            logger.warning("Пагинация не отображается (таймаут)")
            return False

    def get_first_product_price(self):
        logger.info("Получение цены первого товара")
        price_text = self.get_text(self.FIRST_PRODUCT_PRICE)
        price_match = re.search(r'[\d.,]+', price_text)
        if price_match:
            price = float(price_match.group().replace(',', '.'))
            logger.info(f"Цена первого товара: {price}")
            return price
        logger.warning("Цена не найдена")
        return 0.0