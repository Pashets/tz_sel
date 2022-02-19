# -*- coding: utf-8 -*-
from selenium import webdriver
import random
import string
import time
import re
from selenium.webdriver.common.by import By
from xpath_keys import Xpath
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class UkrNet(object):
    link = "https://accounts.ukr.net/login"
    login = "qaautomation"
    password = "132q465w"

    @staticmethod
    def generate_str():
        letters_and_digits = string.ascii_letters + string.digits
        rand_string = ''.join(random.sample(letters_and_digits, 10))
        return rand_string

    def __init__(self):
        self.dict_with_text_and_themes = {}
        self.browser = webdriver.Chrome()
        self.browser.get(self.link)
        self.browser.implicitly_wait(10)

    @staticmethod
    def element_click(element_to_click):
        element_to_click.click()

    def find_element_by_xpath_key(self, element_to_find):
        return self.browser.find_element(By.XPATH, element_to_find)

    def sign_by_login_and_password(self):
        login = self.find_element_by_xpath_key(Xpath.login_xpath)
        login.send_keys(self.login)

        assert self.login == self.find_element_by_xpath_key(Xpath.login_xpath).get_attribute(
            'value'), "Login inputing was failed"
        password = self.find_element_by_xpath_key(Xpath.password_xpath)
        password.send_keys(self.password)
        assert self.password == self.find_element_by_xpath_key(Xpath.password_xpath).get_attribute(
            'value'), "Password inputing was failed"
        sign_in_button = self.find_element_by_xpath_key(Xpath.sign_in_button_xpath)
        self.element_click(sign_in_button)
        assert self.find_element_by_xpath_key(Xpath.incoming_mails_button_xpath)

    def __create_mail_to_my_email_adress(self):
        write_mail_button = self.find_element_by_xpath_key(Xpath.write_mail_button_xpath)
        self.element_click(write_mail_button)
        assert self.find_element_by_xpath_key(Xpath.send_mail_button_xpath)
        my_login = "qaautomation@ukr.net"
        for_whom_input_field = self.find_element_by_xpath_key(Xpath.for_whom_input_field_xpath)
        for_whom_input_field.send_keys(my_login)
        assert self.find_element_by_xpath_key(Xpath.for_whom_input_field_xpath).get_attribute('value') == my_login

    def __create_mail_with_random_10_symbols_in_theme_and_message_text(self):
        self.__create_mail_to_my_email_adress()
        mail_theme_input_field = self.find_element_by_xpath_key(Xpath.mail_theme_input_field_xpath)
        mail_theme = self.generate_str()
        mail_theme_input_field.send_keys(mail_theme)
        assert mail_theme == self.find_element_by_xpath_key(Xpath.mail_theme_input_field_xpath).get_attribute('value')
        mail_text_input_field = self.find_element_by_xpath_key(Xpath.mail_text_input_field_xpath)
        mail_text = self.generate_str()
        mail_text_input_field.send_keys(mail_text)

    def __send_mail(self):
        self.__create_mail_with_random_10_symbols_in_theme_and_message_text()
        send_mail_button = self.find_element_by_xpath_key(Xpath.send_mail_button_xpath)
        self.element_click(send_mail_button)
        assert self.find_element_by_xpath_key("//div[text()=' надіслано']")

    def send_15_created_messages(self):
        self.count_letters_before_sending_mails = int(self.find_element_by_xpath_key("//a[@id='0']//span["
                                                                                     "@class='sidebar__list-link-count']").text)
        for i in range(15):
            self.__send_mail()

    def save_mails_themes_and_messages_in_dict(self):
        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, "//a[@id='0']//span[@class='sidebar__list-link-count']"),
                                             str(self.count_letters_before_sending_mails + 15)))
        incoming_mails_button = self.find_element_by_xpath_key(Xpath.incoming_mails_button_xpath)
        self.element_click(incoming_mails_button)
        assert self.find_element_by_xpath_key("//div[@class='msglist__controls']/a[1]").text == "Переслати"
        for i in range(1, 16):
            key_xpath = "//div[@class='screen__content']//tbody/tr[{}]//td[@class='msglist__row-subject']/a/strong".format(
                i)
            value_xpath = "//div[@class='screen__content']//tbody/tr[{}]//td[@class='msglist__row-subject']/a".format(i)
            list_values = self.find_element_by_xpath_key(value_xpath).text.split('  ')
            self.dict_with_text_and_themes[self.find_element_by_xpath_key(key_xpath).text] = list_values[0]
        return self.dict_with_text_and_themes

    def send_mail_with_dict(self):
        self.__create_mail_to_my_email_adress()
        message_about_mail = ""
        for keys in self.dict_with_text_and_themes:
            message_about_mail += "Received mail on theme {} with message: {}. It contains {} letters and {} numbers \n".format(
                self.dict_with_text_and_themes[keys], keys,
                len([i for i in self.dict_with_text_and_themes[keys] if i.isalpha()]),
                len([i for i in self.dict_with_text_and_themes[keys] if i.isdigit()]))
        mail_text_input_field = self.find_element_by_xpath_key(Xpath.mail_text_input_field_xpath)
        mail_text_input_field.send_keys(message_about_mail)
        send_mail_button = self.find_element_by_xpath_key(Xpath.send_mail_button_xpath)
        self.element_click(send_mail_button)
        assert self.find_element_by_xpath_key("//div[text()=' надіслано']")

    def browser_closing(self):
        self.browser.quit()

    def delete_last_15_created_mails_without_last(self):
        incoming_mails_button = self.find_element_by_xpath_key(Xpath.incoming_mails_button_xpath)
        self.element_click(incoming_mails_button)
        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, "//div[@class='screen__content']//tbody/tr[1]//td["
                                                        "@class='msglist__row-subject']/a/strong"), "Received mail"))
        for i in range(2, 17):
            xpath_key = "//div[@class='screen__content']//tbody/tr[{}]//input".format(i)
            select_mail_checkbox = self.find_element_by_xpath_key(xpath_key)
            self.element_click(select_mail_checkbox)
            assert self.find_element_by_xpath_key(
                "//div[@class='screen__content']//tbody/tr[{}]".format(i)).get_attribute(
                'class') == "msglist__row icon0  ui-draggable checked"
        delete_selected_mails_button = self.find_element_by_xpath_key(Xpath.delete_selected_mails_button_xpath)
        self.element_click(delete_selected_mails_button)
        assert "Повідомлення перенесено в папку " == self.find_element_by_xpath_key("//div[@class='info']")


if __name__ == "__main__":
    brows = UkrNet()
    brows.sign_by_login_and_password()
    brows.send_15_created_messages()
    brows.save_mails_themes_and_messages_in_dict()
    brows.send_mail_with_dict()
    brows.delete_last_15_created_mails_without_last()
    brows.browser_closing()
