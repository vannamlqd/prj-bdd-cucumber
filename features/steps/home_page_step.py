from behave import then, when


@when('We open home page')
def step_impl(context):
    context.page_factory.homepage.open_page()


@then('We should see login form')
def step_impl(context):
    context.page_factory.homepage.verify_visible_of_email_field()\
                                .verify_visible_of_password_field()
