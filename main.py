# -*- coding: utf-8 -*-
from selenium import webdriver
import random
import string
import time


class TestMail():
    link = "https://accounts.ukr.net/login"
    login = "qaautomation"
    password = "132q465w"

    @staticmethod
    def generate_str():
        letters_and_digits = string.ascii_letters + string.digits
        rand_string = ''.join(random.sample(letters_and_digits, 10))
        return rand_string

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.get(self.link)
        self.browser.implicitly_wait(10)

    def sign_by_login_and_password(self):
        login = self.browser.find_element_by_xpath("//input[@type='text']")
        login.send_keys(self.login)
        password = self.browser.find_element_by_xpath("//input[@name='password']")
        password.send_keys(self.password)
        self.browser.find_element_by_xpath("//button[@type='submit']").click()

    def __create_letter_for_my_email_adress(self):
        self.browser.find_element_by_xpath("//button[@class='button primary compose']").click()
        my_login = "qaautomation@ukr.net"
        for_me = self.browser.find_element_by_xpath("//input[@name='toFieldInput']")
        for_me.send_keys(my_login)

    def __create_and_send_letter(self):
        self.__create_letter_for_my_email_adress()
        mail_theme = self.browser.find_element_by_xpath("//input[@name='subject']")
        mail_theme.send_keys(self.generate_str())
        mail_text = self.browser.find_element_by_xpath(
            "//div[@class='mce-edit-area mce-container mce-panel mce-stack-layout-item mce-last']/iframe")
        mail_text.send_keys(self.generate_str())
        self.browser.find_element_by_xpath("//div[@class='sendmsg__bottom-controls']/button[1]").click()
        assert self.browser.find_element_by_xpath("//div[text()=' надіслано']")

    def send_15_created_messages(self):
        for i in range(1, 16):
            self.__create_and_send_letter()

    def save_letters_themes_and_messages_in_dict(self):
        time.sleep(10)
        self.our_dict = {}
        self.browser.find_element_by_xpath("//a[@id='0']").click()
        for i in range(1, 16):
            xpath_key = "//div[@class='screen__content']//tbody/tr[{}]//td[@class='msglist__row-subject']/a/strong".format(
                i)
            xpath_value = "//div[@class='screen__content']//tbody/tr[{}]//td[@class='msglist__row-subject']/a".format(i)
            list_values = self.browser.find_element_by_xpath(
                xpath_value).text.split('  ')
            self.our_dict[self.browser.find_element_by_xpath(xpath_key).text] = list_values[0]
        return self.our_dict

    def send_letter_with_dict(self):
        self.__create_letter_for_my_email_adress()
        message_about_letter = ""
        for keys in self.our_dict:
            message_about_letter += "Received mail on theme {} with message: {}. It contains {} letters and {} numbers \n".format(
                keys, self.our_dict[keys], len([i for i in self.our_dict[keys] if i.isalpha()]),
                len([i for i in self.our_dict[keys] if i.isdigit()]))
        mail_text = self.browser.find_element_by_xpath(
            "//div[@class='mce-edit-area mce-container mce-panel mce-stack-layout-item mce-last']/iframe")
        mail_text.send_keys(message_about_letter)
        self.browser.find_element_by_xpath("//div[@class='sendmsg__bottom-controls']/button[1]").click()

    def delete_last15_created_letters_without_last(self):
        time.sleep(10)
        self.browser.find_element_by_xpath("//a[@id='0']").click()
        for i in range(2, 17):
            xpath_key = "//div[@class='screen__content']//tbody/tr[{}]//input".format(i)
            self.browser.find_element_by_xpath(xpath_key).click()
        self.browser.find_element_by_xpath("//div[@class='msglist__controls']//a[@data-folder='10004']").click()


brows = TestMail()
brows.sign_by_login_and_password()
brows.send_15_created_messages()
brows.save_letters_themes_and_messages_in_dict()
brows.send_letter_with_dict()
brows.delete_last15_created_letters_without_last()
