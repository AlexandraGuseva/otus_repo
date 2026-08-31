from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RegistrationPage(BasePage):
    """Страница регистрации"""

    REGISTRATION_FORM = (By.CSS_SELECTOR, "section.register-form")
    FIRST_NAME = (By.CSS_SELECTOR, "input#field-firstname")
    LAST_NAME = (By.CSS_SELECTOR, "input#field-lastname")
    EMAIL = (By.CSS_SELECTOR, "input#field-email")
    PASSWORD = (By.CSS_SELECTOR, "input#field-password")
    TERMS_CHECKBOX = (By.CSS_SELECTOR, "input#field-optin")

    def is_form_displayed(self):
        return self.wait_for_element(self.REGISTRATION_FORM).is_displayed()

    def is_first_name_displayed(self):
        return self.wait_for_element(self.FIRST_NAME).is_displayed()

    def is_last_name_displayed(self):
        return self.wait_for_element(self.LAST_NAME).is_displayed()

    def is_email_displayed(self):
        return self.wait_for_element(self.EMAIL).is_displayed()

    def is_password_displayed(self):
        return self.wait_for_element(self.PASSWORD).is_displayed()

    def is_terms_displayed(self):
        return self.wait_for_element(self.TERMS_CHECKBOX).is_displayed()