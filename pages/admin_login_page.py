from selenium.webdriver.common.by import By
from pages.base_page import BasePage


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
        self.wait_for_element(self.EMAIL_INPUT).send_keys(email)
        return self

    def enter_password(self, password):
        self.wait_for_element(self.PASSWORD_INPUT).send_keys(password)
        return self

    def click_login_in(self):
        self.click(self.LOGIN_BUTTON)
        return self

    def assert_administration_logged_in(self):
        import time
        time.sleep(5)  #
        assert "login" not in self.driver.current_url.lower()
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