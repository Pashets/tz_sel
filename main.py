from selenium import webdriver
import random
import string


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

    def login_by_login_and_passw(self):
        login = self.browser.find_element_by_xpath("//input[@type='text']")
        login.send_keys(self.login)
        password = self.browser.find_element_by_xpath("//input[@name='password']")
        password.send_keys(self.password)
        self.browser.find_element_by_xpath("//button[@type='submit']").click()


    def create_letter_for_me(self):
        self.browser.find_element_by_xpath("//button[@class='button primary compose']").click()
        my_login = "qaautomation@ukr.net"
        for_me = self.browser.find_element_by_xpath("//input[@name='toFieldInput']")
        for_me.send_keys(my_login)

    def create_and_send_letter(self):
        self.create_letter_for_me()
        mail_theme = self.browser.find_element_by_xpath("//input[@name='subject']")
        mail_theme.send_keys(self.generate_str())
        mail_text = self.browser.find_element_by_xpath(
            "//div[@class='mce-edit-area mce-container mce-panel mce-stack-layout-item mce-last']/iframe")
        mail_text.send_keys(self.generate_str())
        self.browser.find_element_by_xpath("//div[@class='sendmsg__bottom-controls']/button[1]").click()
        assert self.browser.find_element_by_xpath("//div[text()=' надіслано']")

    def send_15_messages(self):
        for i in range(1, 16):
            self.create_and_send_letter()

    def contain_in_dict(self):
        self.our_dict = {}
        self.browser.find_element_by_xpath("//a[@id='0']").click()
        for i in range(1, 16):
            xpath_key = f"//tbody/tr[{i}]//td[@class='msglist__row-subject']/a/strong"
            xpath_value = f"//tbody/tr[{i}]//td[@class='msglist__row-subject']/a/strong/parent::a"
            list_1 = self.browser.find_element_by_xpath(
                xpath_value).text.split('  ')
            self.our_dict[self.browser.find_element_by_xpath(xpath_key).text] = list_1[0]
        return self.our_dict

    def last_letter(self):
        self.create_letter_for_me()
        str_1 = f""
        for keys in self.our_dict:
            str_1 += f"Received mail on theme {keys} with message: {self.our_dict[keys]}. It contains {len([i for i in self.our_dict[keys] if i.isalpha()])} letters and {len([i for i in self.our_dict[keys] if i.isdigit()])} numbers \n"
        mail_text = self.browser.find_element_by_xpath(
            "//div[@class='mce-edit-area mce-container mce-panel mce-stack-layout-item mce-last']/iframe")
        mail_text.send_keys(str_1)
        self.browser.find_element_by_xpath("//div[@class='sendmsg__bottom-controls']/button[1]").click()

    def delete_my_letters(self):
        self.browser.find_element_by_xpath("//a[@id='0']").click()
        for i in range(16):
            xpath_key = f"//tbody/tr[2]//input"
            self.browser.find_element_by_xpath(xpath_key).click()
            self.browser.find_element_by_xpath("//div[@class='msglist__controls']//a[@data-folder='10004']").click()


brows = TestMail()
brows.login_by_login_and_passw()
brows.send_15_messages()
brows.contain_in_dict()
brows.last_letter()
brows.delete_my_letters()
