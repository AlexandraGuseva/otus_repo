import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)


class BasePage:
    """Базовый класс для всех страниц. Содержит общие методы."""

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(self.driver, 10)

    def open(self, url=""):
        full_url = url if url.startswith("http") else self.base_url + url
        logger.info(f"Открываем URL: {full_url}")
        self.driver.get(full_url)
        return self

    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_presence(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_elements(self, locator, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located(locator)
            )
            logger.debug(f"Найдено элементов {locator}: {len(elements)}")
            return elements
        except TimeoutException:
            logger.warning(f"Элементы не найдены за {timeout} сек: {locator}")
            return []

    def click(self, locator, timeout=10):
        try:
            element = self.wait_for_clickable(locator, timeout)
            element.click()
            return self
        except Exception as e:
            logger.error(f"Не удалось кликнуть по {locator}: {e}")
            raise

    def get_text(self, locator, timeout=10):
        text = self.wait_for_element(locator, timeout).text
        logger.debug(f"Получен текст из {locator}: {text[:50]}")
        return text

    def is_displayed(self, locator, timeout=10):
        try:
            return self.wait_for_element(locator, timeout).is_displayed()
        except TimeoutException:
            return False

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url