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

    def switch_to_iframe(self):
        """Переключение на iframe (если есть)"""
        print("ℹ️   iframe не используется, работаем напрямую")
        return self

    def find_element(self, locator, timeout=10):
        """Явное ожидание видимости элемента (один элемент)"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            return self.driver.find_element(*locator)

    def find_elements(self, locator, timeout=10):
        """Явное ожидание видимости элементов (список)"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located(locator)
            )
        except TimeoutException:
            return self.driver.find_elements(*locator)

    def click(self, locator, timeout=10):
        """Клик по элементу с ожиданием кликабельности"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        return self

    def get_text(self, locator, timeout=10):
        """Получение текста элемента"""
        return self.find_element(locator, timeout).text

    def is_displayed(self, locator, timeout=10):
        """Проверяет, отображается ли элемент"""
        try:
            return self.find_element(locator, timeout).is_displayed()
        except:
            return False

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url

    def wait_for_element(self, locator, timeout=10):
        """Ждёт, пока элемент станет видимым"""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=10):
        """Ждёт, пока элемент станет кликабельным"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_presence(self, locator, timeout=10):
        """Ждёт, пока элемент появится в DOM"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )