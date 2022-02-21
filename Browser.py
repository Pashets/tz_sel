# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By



class Browser(object):
    link = "https://accounts.ukr.net/login"

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.get(self.link)
        self.browser.implicitly_wait(10)

    def browser_closing(self):
        self.browser.quit()

    @staticmethod
    def element_click(element_to_click):
        element_to_click.click()

    def find_element_by_xpath_key(self, element_to_find):
        return self.browser.find_element(By.XPATH, element_to_find)