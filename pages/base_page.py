from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Базовый класс для всех страниц. Содержит общие методы."""

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(self.driver, 10)

    def open(self, url=""):
        """Открывает страницу по относительному URL"""
        if url.startswith("http"):
            self.driver.get(url)
        else:
            self.driver.get(self.base_url + url)
        return self

    def wait_for_element(self, locator, timeout=10):
        """Ожидает видимость элемента."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=10):
        """Ожидает, что элемент станет кликабельным"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_presence(self, locator, timeout=10):
        """Ожидает появления элемента в DOM"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def click(self, locator, timeout=10):
        """Клик по элементу с ожиданием кликабельности"""
        element = self.wait_for_clickable(locator, timeout)
        element.click()
        return self

    def get_text(self, locator, timeout=10):
        """Получение текста элемента"""
        return self.wait_for_element(locator, timeout).text

    def is_displayed(self, locator, timeout=10):
        """Проверяет - отображается ли элемент"""
        try:
            return self.wait_for_element(locator, timeout).is_displayed()
        except TimeoutException:
            return False

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url