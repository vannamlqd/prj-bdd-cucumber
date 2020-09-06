'''
Created on Apr 25, 2019

@author: Thang Nguyen
'''
import os
import configparser

# Config
conf = configparser.RawConfigParser()
conf.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "selenium.properties"))

# Timeout
implicit_timeout = conf.getint("webdriver", "timeouts.implicitwait")
explicit_timeout = conf.getint("webdriver", "timeouts.explicitwait")

# Chrome
CHROME = "chrome"
chrome_driver_name = conf.get("webdriver", "chrome.driver")
# Ie
IE = "ie"
ie_driver_name = conf.get("webdriver", "ie.driver")
# Edge
EDGE = "edge"
edge_driver_name = conf.get("webdriver", "edge.driver")
# Firefox
FIREFOX = "firefox"
firefox_driver_name = conf.get("webdriver", "firefox.driver")
# Safari
# safari = "safari"
executing_driver = conf.get("webdriver", "execute.driver")
# Browser available to test
browser_list = conf.get("webdriver", "drivers").replace(" ", "").split(",")  

# Path to browser drivers
driver_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "selenium_project", "drivers")
chrome_driver = os.path.join(driver_dir, chrome_driver_name)
ie_driver = os.path.join(driver_dir, ie_driver_name)
edge_driver = os.path.join(driver_dir, edge_driver_name)
firefox_driver = os.path.join(driver_dir, firefox_driver_name)

# Screenshot
AFTER_EACH_ACTION = "AFTER_EACH_ACTION"  # Capture screenshot after each action
FOR_FAILURES = "FOR_FAILURES"  # Capture screenshot on failures only
DISABLED = "DISABLED"  # No capture
capture_mode = conf.get("features", "screenshot")
DESKTOP = "DESKTOP"
BROWSER = "BROWSER"
capture_on = conf.get("features", "screenshots.on")

# Other config
