from web.core import driver
from time import sleep
from web.core import selenium_config
from web.pageobjects.page_factory import web_pages

IDLE_TIMER = 3


# Hooks
def before_all(context):
    context.config.setup_logging()
    driver.start_browser(context, browser_type=selenium_config.CHROME)
    web_pages(context)


def after_all(context):
    # TODO
    # uninstall the app on cloude device
    # context.driver.remove_app(context.config.userdata.get("app_uri"));
    pass


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    # start_activity()
    # Android ONLY
    # get_current_activity()
    pass


def after_scenario(context, scenario):
    # TODO
    pass


def after_feature(context, feature):
    driver.close_driver(context)


def before_step(context, step):
    pass


def after_step(context, step):
    if step.status == "failed":
        # Take screenshot
        # ts = time.time()
        # st = time.ctime(ts)
        # screenshot_file = gSCREEN_SHOTS_PATH + step.name + "_" + st + ".png"
        # take_screenshot(context, screenshot_file)
        # allure.attach(context.driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
        sleep(IDLE_TIMER)
    pass


def before_tag(context, tag):
    pass


def after_tag(context, tag):
    pass
