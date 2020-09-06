from web.pageobjects.home_page import HomePage


def web_pages(context):
    context.page_factory = PageFactory(context)


class PageFactory(object):
    def __init__(self, context):
        self.__homepage = HomePage(context)

    @property
    def homepage(self):
        return self.__homepage
