from web.core.sele_libs import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    def __init__(self, context):
        super().__init__(context)

    WEB_URL = "https://telesense.app/"
    TXT_EMAIL_ADDRESS = (By.XPATH, "//label[text()='Email address']/following-sibling::input")
    TXT_PASSWORD = (By.XPATH, "//label[text()='Password']/following-sibling::input")

    def open_page(self):
        self.open_url(self.WEB_URL)
        return self

    def verify_visible_of_email_field(self):
        self.element(self.TXT_EMAIL_ADDRESS).wait_until_visible()
        return self

    def enter_email(self, email):
        self.element(self.TXT_EMAIL_ADDRESS).wait_until_clickable().send_keys(email)
        return self

    def enter_password(self, password):
        self.element(self.TXT_PASSWORD).wait_until_clickable().send_keys(password)
        return self

    def verify_visible_of_password_field(self):
        self.element(self.TXT_PASSWORD).wait_until_visible()
        return self
