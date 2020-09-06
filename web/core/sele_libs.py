'''
Created on Apr 25, 2019

@author: Thang Nguyen
'''

from time import sleep

from selenium.common.exceptions import TimeoutException, NoSuchElementException, \
    StaleElementReferenceException, ElementNotInteractableException, \
    ElementNotVisibleException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

from utils.logger import logger
# from utils.date_utils import get_timestamp
from web.core.selenium_config import explicit_timeout, executing_driver
from web.core.driver import start_browser


class BasePage(object):

    @property
    def browser(self):
        return self.__browser

    @browser.setter
    def browser(self, browser):
        self.__browser = browser

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, logger):
        self.__logger = logger

    def __init__(self, context):
        self.logger = logger
        self.browser = context.browser

    def find_element(self, *args):
        try:
            return self.browser.find_element(*args)
        except(TimeoutException, NoSuchElementException, StaleElementReferenceException,
               ElementNotVisibleException, ElementNotInteractableException) as e:
            raise Exception(
                self.logger.debug("[TEST FAILED]: The element located by {0}: '{1}' need to check".format(*args)))

    def find_elements(self, *args):
        return self.browser.find_elements(*args)

    def get_text_values(self, *locator):
        items = [x for x in self.find_elements(*locator)]
        list_value = []
        for item in items:
            list_value.append(item.text)
        return list_value

    def size(self):
        return len(self.find_elements(self._by, self._value))

    def is_present(self):
        if self.size() > 0:
            return True
        else:
            return False

    def is_visible(self):
        if self.find_element(self._by, self._value).is_displayed():
            return True
        else:
            return False

    def open_url(self, url):
        logger.info("Opening URL: {0}".format(url))
        self.browser.get(url)
        return self

    def close(self):
        self.browser.quit()

    def element(self, locator):
        logger.info("Locator: {0}".format(locator))
        self._by = locator[0]
        self._value = locator[1]
        return self

    def wait_until_clickable(self, timeout=explicit_timeout):
        logger.info("Wait for element is clickable in {0}".format(timeout))
        splited_timeout = timeout / 3
        wait = WebDriverWait(self.browser, splited_timeout)
        # Thang: Set implicitly wait to be same as explicit wait 
        self.browser.implicitly_wait(splited_timeout)
        for i in range(3):
            try:
                wait.until(EC.element_to_be_clickable((self._by, self._value)))
                self.browser.implicitly_wait(20)
                return self
            except(TimeoutException, NoSuchElementException):
                if i == 2:
                    self.browser.implicitly_wait(20)
                    raise

    def wait_until_visible(self, timeout=explicit_timeout):
        logger.info("Wait for element is visible in {0}".format(timeout))
        splited_timeout = timeout / 3
        wait = WebDriverWait(self.browser, splited_timeout)
        # Thang: Set implicitly wait to be same as explicit wait 
        self.browser.implicitly_wait(splited_timeout)
        for i in range(3):
            try:
                wait.until(EC.visibility_of_element_located((self._by, self._value)))
                self.browser.implicitly_wait(20)
                return self
            except(TimeoutException, NoSuchElementException):
                if i == 2:
                    self.browser.implicitly_wait(20)
                    raise

    def wait_until_invisible(self, timeout=explicit_timeout):
        logger.info("Wait for element is invisible in {0}".format(timeout))
        try:
            wait = WebDriverWait(self.browser, timeout)
            wait.until_not(EC.visibility_of_element_located((self._by, self._value)))
            return self
        except(TimeoutException):
            raise

    def wait_until_present(self, timeout=explicit_timeout):
        logger.info("Wait for element is present in {0}".format(timeout))
        splited_timeout = timeout / 3
        wait = WebDriverWait(self.browser, splited_timeout)
        for i in range(3):
            try:
                wait.until(EC.presence_of_element_located((self._by, self._value)))
                return self
            except(TimeoutException, Exception):
                if i == 2:
                    raise

    def wait_until_not_present(self, timeout=explicit_timeout):
        logger.info("Wait for element is not present in {0}".format(timeout))
        try:
            wait = WebDriverWait(self.browser, timeout)
            wait.until_not(EC.presence_of_element_located((self._by, self._value)))
            return self
        except(TimeoutException, Exception):
            raise

    def wait_for_text_to_appear(self, text, timeout=explicit_timeout):
        try:
            wait = WebDriverWait(self.browser, timeout)
            wait.until(EC.text_to_be_present_in_element((self._by, self._value), text))
            return self
        except(TimeoutException, Exception):
            raise

    def click(self):
        logger.info("Click into element")
        self.find_element(self._by, self._value).click()
        return self

    def get_width(self):
        element = self.find_element(self._by, self._value).size
        return element.get("width")

    def get_height(self):
        element = self.find_element(self._by, self._value).size
        return element.get("height")

    def click_and_wait(self, timeout=3):
        logger.info("Click into element and wait {0}".format(timeout))
        self.find_element(self._by, self._value).click()
        self.delay(timeout)
        return self

    def send_keys(self, value):
        logger.info("Send Keys: {0}".format(value))
        self.find_element(self._by, self._value).send_keys(value)
        return self

    def type_and_wait(self, value, timeout=3):
        logger.info("Send Keys: {0} then wait {1}".format(value, str(timeout)))
        self.find_element(self._by, self._value).send_keys(value)
        self.delay(timeout)
        return self

    def implicitly_wait(self, *args):
        return self.browser.implicitly_wait(*args)

    def get_title(self):
        return self.browser.title

    def enter_text_into(self, value, *locator):
        self.find_element(*locator).send_keys(value)
        return self

    def text(self):
        text = self.find_element(self._by, self._value).text
        logger.info("Element text: {0}".format(text))
        return text

    def get_value(self):
        value = self.get_attribute_value("value")
        logger.info("Element value: {0}".format(value))
        return value

    def get_attribute_value(self, attribute):
        value = self.find_element(self._by, self._value).get_attribute(attribute)
        return value

    # Using for td tag

    def get_text_by_innerhtml(self):
        return self.find_element(self._by, self._value).get_attribute("innerHTML")

    def get_text_by_value(self):
        return self.find_element(self._by, self._value).get_attribute("value")

    def clear(self):
        self.find_element(self._by, self._value).clear()
        return self

    def click_on_element(self, *locator):
        self.find_element(*locator).click()
        return self

    def get_source_html(self):
        return self.browser.page_source

    def get_current_url(self):
        url = self.browser.current_url
        logger.info("Current url: {0}".format(url))
        return url

    def accept_alert(self, alert_text=None):
        logger.info("Accept alert with text: {0}".format(alert_text))
        WebDriverWait(self.browser, 30).until(EC.alert_is_present(), 'Timed out waiting for PA creation '
                                              + 'confirmation popup to appear.')

        popup = self.browser.switch_to.alert
        if alert_text:
            msg = "Verify alert text equals: {0}".format(alert_text)
            self.logger.debug(msg)
            if popup.text != alert_text:
                msg = "Alert text is: {0} - doesn't match".format(popup.text())
                self.logger.debug(msg)
        popup.accept()
        return self

    def dismiss_alert(self, alert_text=None):
        logger.info("Dismiss alert with text: {0}".format(alert_text))
        WebDriverWait(self.browser, 30).until(EC.alert_is_present(), 'Timed out waiting for PA creation '
                                              + 'confirmation popup to appear.')

        popup = self.browser.switch_to.alert
        if alert_text:
            msg = "Verify alert text equals: {0}".format(alert_text)
            self.logger.debug(msg)
            if popup.text != alert_text:
                msg = "Alert text is: {0} - doesn't match".format(popup.text)
                self.logger.debug(msg)
        popup.dismiss()
        return self

    def select_option_by_text(self, value):
        logger.info("Select option with text: {0}".format(value))
        Select(self.find_element(self._by, self._value)).select_by_visible_text(value)
        return self

    def select_option_by_value(self, value):
        logger.info("Select option with value: {0}".format(value))
        Select(self.find_element(self._by, self._value)).select_by_value(value)
        return self

    def select_option_by_index(self, value):
        logger.info("Select option with index: {0}".format(value))
        Select(self.find_element(self._by, self._value)).select_by_index(value)
        return self

    def get_selected_visible_text_value(self):
        return Select(self.find_element(self._by, self._value)).first_selected_option.get_attribute("innerText")

    def get_selected_value(self):
        return Select(self.find_element(self._by, self._value)).first_selected_option.get_attribute("value")

    def getdriver(self):
        return self.browser

    def refresh_page(self):
        logger.info("Refresh page")
        self.browser.refresh()
        return self

    def is_checked(self):
        """
        Check the radio or checkbox status
        :return:
            None: If the object is unchecked
            true: If the object is checked
        """
        return self.get_attribute_value("checked")

    def check(self):
        if self.is_checked() is None:
            self.click()
        return self

    def un_check(self):
        if self.is_checked() is not None:
            self.click()
        return self

    def evaluate_javascript(self, js, *args):
        return self.browser.execute_script(js, *args)

    def highlight_element(self):
        element = self.find_element(self._by, self._value)

        def apply_style(s):
            self.evaluate_javascript("arguments[0].setAttribute('style', arguments[1]);", element, s)

        original_style = self.get_attribute_value('style')
        apply_style("background: yellow; border: 2px solid red;")
        sleep(.3)
        apply_style(original_style)
        return self

    def delay(self, seconds):
        sleep(seconds)
        return self

    def minimize_browser(self):
        self.browser.set_window_position(-2000, 0)
        sleep(1)
        return self

    def maximize_browser(self):
        self.browser.set_window_position(0, 0)  # Move browser to top left
        sleep(1)
        return self
