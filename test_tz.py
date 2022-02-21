from UkrNet import UkrNet
from UkrNet import Browser
from selenium import webdriver
import pytest
from xpath_keys import Xpath
import selenium.common.exceptions


@pytest.fixture(scope='class')
def browser():
    browser = UkrNet()
    yield browser
    Browser.browser_closing(browser)


class Test_tz_project():

    def test_should_be_right_profile_after_sign_in(self, browser):
        browser.sign_by_login_and_password()
        assert browser.find_element_by_xpath_key(
            "//p[@class='login-button__user']").text == "qaautomation@ukr.net", "incorrect profile"
