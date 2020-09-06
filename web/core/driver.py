'''
Created on Apr 25, 2019

@author: Thang Nguyen
'''

import os
import shutil
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# from utils.logger import #log_info
from web.core.selenium_config import implicit_timeout, browser_list, \
    CHROME, IE, EDGE, FIREFOX, \
    chrome_driver, ie_driver, \
    edge_driver, firefox_driver


# Remove data on edge browser
def clear_edge_browser_data():
    appdata_location = os.environ.get('LOCALAPPDATA')
    _edge_temp_dir = r"{0}\Packages\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\AC".format(
        appdata_location)
    _edge_app_data = r"{0}\Packages\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\AppData".format(
        appdata_location)

    try:
        os.system("taskkill  /F /IM MicrosoftEdge.exe")
    except:
        pass
    try:
        os.system("taskkill  /F /IM dllhost.exe")
    except:
        pass
    if os.path.exists(_edge_temp_dir):
        for directory in os.listdir(_edge_temp_dir):
            if directory.startswith('#!'):
                shutil.rmtree(
                    os.path.join(_edge_temp_dir, directory), ignore_errors=True)

    if os.path.exists(_edge_app_data):
        shutil.rmtree(_edge_app_data, ignore_errors=True)


def start_chrome():
    option = webdriver.ChromeOptions()
    prefs = {'safebrowsing.enabled': 'false'}  # To accept file download
    option.add_experimental_option("prefs", prefs)
    option.add_argument("--disable-web-security")  # Enable using JS on IFrame
    option.add_argument('--ignore-certificate-errors')  # Ignore SSL
    option.add_argument("--incognito")  # Private mode, won't save any history
    driver_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                               "resources", "drivers", "chromedriver")
    browser = webdriver.Chrome(executable_path=driver_path,
                               chrome_options=option)

    sleep(2)
    browser.set_window_position(0, 0)  # Move browser to top left
    sleep(1)
    # log_info("Maximize browser size")
    browser.maximize_window()
    sleep(1)
    return browser


def start_edge():
    clear_edge_browser_data()
    sleep(5)
    browser = webdriver.Edge(edge_driver)
    sleep(2)
    browser.set_window_position(0, 0)  # Move browser to top left
    sleep(1)
    # log_info("Resize")
    browser.set_window_size(1024, 768)
    sleep(3)
    return browser


def start_firefox():
    ffCab = DesiredCapabilities.FIREFOX
    ffCab["marionette"] = True
    browser = webdriver.Firefox(capabilities=ffCab,
                                executable_path=firefox_driver)

    # log_info("Maximize browser size")
    browser.maximize_window()
    return browser


def start_ie():
    return webdriver.Ie(ie_driver)


def start_browser(context, browser_type=CHROME):
    browser = None
    try:
        if browser_type in browser_list:
            pass
            # log_info("Opening browser:" + browser_type)
        else:
            # log_info("Not support, use Chrome as default")
            browser_type = CHROME  # Open chrome for non-support browser
        if browser_type == IE:
            browser = start_ie()
        elif browser_type == CHROME:
            browser = start_chrome()
        elif browser_type == EDGE:
            browser = start_edge()
        elif browser_type == FIREFOX:
            browser = start_firefox()
        browser.implicitly_wait(implicit_timeout)

        context.browser = browser
        # log_info("Browser is opened")
    except Exception as e:
        raise e


def close_driver(context):
    context.browser.quit()


def capture_screenshot(context, ss_name, dst=None):
    try:
        if dst:  # Capture to a folder
            screenshot_dst = os.path.join(dst, ss_name)
        else:  # Capture to default folder
            pass

        context.browser.save_screenshot(screenshot_dst)
        return True
    except:  # alert occurs or browser not started then we should capture desktop
        return False
