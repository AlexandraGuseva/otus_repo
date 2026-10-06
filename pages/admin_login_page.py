import logging
import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class AdminLoginPage(BasePage):
    """Страница входа в админку PrestaShop"""

    LOGO = (By.CSS_SELECTOR, "img[alt='PrestaShop'], .brand img")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email'], input#email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password'], input#passwd")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], button#submit_login")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "#forgot-password-link")

    def open_admin_page(self):
        self.open("/admin-dev")
        return self

    def enter_email(self, email):
        logger.info(f"Ввод email администратора: {email}")
        self.wait_for_element(self.EMAIL_INPUT).send_keys(email)
        return self

    def enter_password(self, password):
        self.wait_for_element(self.PASSWORD_INPUT).send_keys(password)
        return self

    def click_login_in(self):
        self.click(self.LOGIN_BUTTON)
        return self

    def assert_administration_logged_in(self):
        time.sleep(5)
        current_url = self.driver.current_url
        logger.info(f"Проверка входа. Текущий URL: {current_url}")
        assert "login" not in current_url.lower(), "Не удалось войти в админку"
        logger.info("Вход в админку выполнен успешно")
        return self

    def is_logo_displayed(self):
        return self.is_displayed(self.LOGO)

    def is_email_input_displayed(self):
        return self.is_displayed(self.EMAIL_INPUT)

    def is_password_input_displayed(self):
        return self.is_displayed(self.PASSWORD_INPUT)

    def is_login_button_displayed(self):
        return self.is_displayed(self.LOGIN_BUTTON)

    def is_forgot_password_link_displayed(self):
        return self.is_displayed(self.FORGOT_PASSWORD_LINK)