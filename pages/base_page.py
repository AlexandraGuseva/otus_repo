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
        logger.info(f"Инициализирована страница: {self.__class__.__name__}")

    def open(self, url=""):
        full_url = url if url.startswith("http") else self.base_url + url
        logger.info(f"Открываем URL: {full_url}")
        self.driver.get(full_url)
        return self

    def wait_for_element(self, locator, timeout=10):
        logger.info(f"Ожидание видимости элемента: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=10):
        logger.info(f"Ожидание кликабельности элемента: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_presence(self, locator, timeout=10):
        logger.info(f"Ожидание появления элемента в DOM: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

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

    def click(self, locator, timeout=10):
        logger.info(f"Клик по элементу: {locator}")
        element = self.wait_for_clickable(locator, timeout)
        element.click()
        logger.info("Клик выполнен успешно")
        return self

    def get_text(self, locator, timeout=10):
        logger.info(f"Получение текста элемента: {locator}")
        text = self.wait_for_element(locator, timeout).text
        logger.info(f"Текст получен: {text[:50]}")
        return text

    def is_displayed(self, locator, timeout=10):
        logger.info(f"Проверка отображения элемента: {locator}")
        try:
            result = self.wait_for_element(locator, timeout).is_displayed()
            logger.info(f"Элемент отображается: {result}")
            return result
        except TimeoutException:
            logger.warning(f"Элемент не отобразился за {timeout} секунд: {locator}")
            return False

    def get_title(self):
        title = self.driver.title
        logger.info(f"Заголовок страницы: {title}")
        return title

    def get_current_url(self):
        url = self.driver.current_url
        logger.info(f"Текущий URL: {url}")
        return url