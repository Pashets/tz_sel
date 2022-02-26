# -*- coding: utf-8 -*-
from selenium import webdriver
import random
import os
import string
from selenium.webdriver.common.by import By
from xpath_keys import Xpath
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Browser import Browser


class UkrNet(Browser):
    login = "qaautomation"  # здесь в ковычках пишите вашу почту на укр нете без добавленя @ukr.net
    password = "132q465w"  # здесь в ковычках пароль

    def add_file(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(current_dir, 'IMG_0647.MP4')
        add_video = Browser.find_element_by_xpath_key(self, Xpath.add_videofile)
        add_video.send_keys(file_path)

    @staticmethod
    def generate_str():
        letters_and_digits = string.ascii_letters + string.digits
        rand_string = ''.join(random.sample(letters_and_digits, 10))
        return rand_string

    def __init__(self):
        Browser.__init__(self)
        self.dict_with_text_and_themes = {}

    def input_login(self):
        login = Browser.find_element_by_xpath_key(self, Xpath.login_xpath)
        login.send_keys(self.login)
        assert self.login == Browser.find_element_by_xpath_key(self, Xpath.login_xpath).get_attribute(
            'value'), "Login inputing was failed"

    def input_password(self):
        password = Browser.find_element_by_xpath_key(self, Xpath.password_xpath)
        password.send_keys(self.password)
        assert self.password == Browser.find_element_by_xpath_key(self, Xpath.password_xpath).get_attribute(
            'value'), "Password inputing was failed"

    def sign_by_login_and_password(self):
        self.input_login()
        self.input_password()
        sign_in_button = Browser.find_element_by_xpath_key(self, Xpath.sign_in_button_xpath)
        Browser.element_click(sign_in_button)
        assert Browser.find_element_by_xpath_key(self, Xpath.incoming_mails_button_xpath)

    def go_to_writing_mail_page(self):
        write_mail_button = Browser.find_element_by_xpath_key(self, Xpath.write_mail_button_xpath)
        Browser.element_click(write_mail_button)
        assert Browser.find_element_by_xpath_key(self, Xpath.send_mail_button_xpath)

    def input_for_whom_mail(self, login):
        for_whom_input_field = Browser.find_element_by_xpath_key(self, Xpath.for_whom_input_field_xpath)
        for_whom_input_field.send_keys(login)
        assert Browser.find_element_by_xpath_key(self, Xpath.for_whom_input_field_xpath).get_attribute('value') == login

    def __create_mail_to_my_email_adress(self):
        self.go_to_writing_mail_page()
        my_login = "r77-secretar@russianpost.ru"  # здесь ввести почту которую хотите заспамить
        self.input_for_whom_mail(my_login)

    def input_mail_theme(self):
        mail_theme_input_field = Browser.find_element_by_xpath_key(self, Xpath.mail_theme_input_field_xpath)
        mail_theme = "Россиянам"
        mail_theme_input_field.send_keys(mail_theme)
        assert mail_theme == Browser.find_element_by_xpath_key(self, Xpath.mail_theme_input_field_xpath).get_attribute(
            'value')

    def __create_mail_with_random_10_symbols_in_theme_and_message_text(self):
        self.__create_mail_to_my_email_adress()
        self.input_mail_theme()
        self.input_mail_text(
            "Либо ваша армия вернется в россию либо окажется уничтоженнй, на пару с вашей экономикой и жизнью, подумайте")

    def input_mail_text(self, text):
        mail_text_input_field = Browser.find_element_by_xpath_key(self, Xpath.mail_text_input_field_xpath)
        mail_text_input_field.send_keys(text)

    def __send_mail(self):
        self.__create_mail_with_random_10_symbols_in_theme_and_message_text()
        self.send_mail_button_click()

    def send_1000_created_messages(self):
        # self.count_letters_before_sending_mails = int(Browser.find_element_by_xpath_key(self, "//a[@id='0']//span["
        #                                                                                      "@class='sidebar__list-link-count']").text)
        for i in range(1000):
            self.__send_mail()

    def go_to_incoming_mails_page(self):
        incoming_mails_button = Browser.find_element_by_xpath_key(self, Xpath.incoming_mails_button_xpath)
        Browser.element_click(incoming_mails_button)
        assert Browser.find_element_by_xpath_key(self, "//div[@class='msglist__controls']/a[1]").text == "Переслати"

        # def save_mails_themes_and_messages_in_dict(self):
        #    WebDriverWait(self.browser, 10).until(
        #        EC.text_to_be_present_in_element((By.XPATH, "//a[@id='0']//span[@class='sidebar__list-link-count']"),
        #                                         str(self.count_letters_before_sending_mails + 15)))
        self.go_to_incoming_mails_page()
        for i in range(1, 16):
            key_xpath = "//div[@class='screen__content']//tbody/tr[{}]//td[@class='msglist__row-subject']/a/strong".format(
                i)
            value_xpath = "//div[@class='screen__content']//tbody/tr[{}]//td[@class='msglist__row-subject']/a".format(i)
            list_values = Browser.find_element_by_xpath_key(self, value_xpath).text.split('  ')
            self.dict_with_text_and_themes[Browser.find_element_by_xpath_key(self, key_xpath).text] = list_values[0]
        return self.dict_with_text_and_themes

    def send_mail_button_click(self):
        send_mail_button = Browser.find_element_by_xpath_key(self, Xpath.send_mail_button_xpath)
        Browser.element_click(send_mail_button)
        assert Browser.find_element_by_xpath_key(self, "//div[text()=' надіслано']")

    def send_mail_with_dict(self):
        self.__create_mail_to_my_email_adress()
        message_about_mail = ""
        for key in self.dict_with_text_and_themes:
            message_about_mail += "Received mail on theme {} with message: {}. It contains {} letters and {} numbers \n".format(
                self.dict_with_text_and_themes[key], key,
                len([i for i in self.dict_with_text_and_themes[key] if i.isalpha()]),
                len([i for i in self.dict_with_text_and_themes[key] if i.isdigit()]))
        self.input_mail_text(message_about_mail)
        self.send_mail_button_click()

    def delete_selected_mails(self):
        delete_selected_mails_button = Browser.find_element_by_xpath_key(self, Xpath.delete_selected_mails_button_xpath)
        Browser.element_click(delete_selected_mails_button)
        assert "Видалені" == Browser.find_element_by_xpath_key(self, "//div[@class='info show']/a").text

    def select_mail(self, mail_number):
        xpath_key = "//div[@class='screen__content']//tbody/tr[{}]//input".format(mail_number)
        select_mail_checkbox = Browser.find_element_by_xpath_key(self, xpath_key)
        Browser.element_click(select_mail_checkbox)
        assert Browser.find_element_by_xpath_key(self,
                                                 "//div[@class='screen__content']//tbody/tr[{}]".format(
                                                     mail_number)).get_attribute(
            'class') == "msglist__row unread icon0  ui-draggable checked"

    def delete_last_15_created_mails_without_last(self):
        self.go_to_incoming_mails_page()
        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, "//div[@class='screen__content']//tbody/tr[1]//td["
                                                        "@class='msglist__row-subject']/a/strong"), "Received mail"))
        for i in range(2, 17):
            self.select_mail(i)
        self.delete_selected_mails()


if __name__ == "__main__":
    ukrnet = UkrNet()
    ukrnet.sign_by_login_and_password()
    ukrnet.send_1000_created_messages()
    # ukrnet.save_mails_themes_and_messages_in_dict()
    # ukrnet.send_mail_with_dict()
    # ukrnet.delete_last_15_created_mails_without_last()
    ukrnet.browser_closing()
