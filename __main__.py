from time import sleep
from os import listdir
from random import choice

from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from database import DataBase
from gologin import GoLogin
from logger import logger

URL = 'https://1sex24sex.com/add'
LOGGER = logger(__name__, 'w')


class Sex24:
    def __init__(self, contact, index):
        self.contact = contact
        self.index = index
        self.gl = GoLogin(dict(token=DataBase.GOLOGIN_APIKEY))
        host, port = DataBase.df['proxy'].dropna().tolist()[index].split(':')
        # host, port = '109.248.7.197:11967'.split(':')
        self.profile_id = self.gl.create({
            "proxy": {
                "mode": "http",
                "host": host,
                "port": port,
            },
        })
        self.gl.setProfileId(self.profile_id)
        self.debugger_address = self.gl.start()
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", self.debugger_address)
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(900, 900)
        self.driver.get(URL)

    def captcha_solver(self, captcha_key):
        print('solving captcha')
        payload = dict(key=DataBase.RUCAPTCHA_APIKEY,
                       method='userrecaptcha', googlekey=captcha_key, pageurl=DataBase.URL, json=1)
        req = get('http://rucaptcha.com/in.php', params=payload)

        payload = dict(key=DataBase.RUCAPTCHA_APIKEY,
                       action='get', id=req.json()['request'], json=1)
        while True:
            req = get('http://rucaptcha.com/res.php', params=payload)
            if req.json()['status']:
                return req.json()['request']

    def upload_photo(self, image_input_xpath):  # fix
        images_path = r'C:\Users\KIEV-COP-4\Desktop\RussianDoska\home\danil\images'
        random_image = images_path + choice([file for file in listdir(images_path) if file.endswith('jpg')])
        self.driver.find_element_by_xpath(image_input_xpath).send_keys(random_image)

    def spam(self):  # todo photo upload
        editor_title = '//*[@id="editor_title"]'
        header = choice(DataBase.df['title'].dropna().tolist())
        WebDriverWait(self.driver, 10).until(
            lambda d: self.driver.find_element(By.XPATH, editor_title)).send_keys(header)
        editor = '//*[@id="editor"]'
        text = choice(DataBase.df['description'].dropna().tolist())
        self.driver.find_element_by_xpath(editor).send_keys(text)
        contact_xpath = '//*[@name="email"]'
        self.driver.find_element_by_xpath(contact_xpath).send_keys(self.contact)
        # image_xpath = '//*[@id="image-upload-1"]'
        # self.upload_photo(image_xpath)
        captcha_xpath = '//*[@id="add-ad-form"]/div[8]'
        data_sitekey = self.driver.find_element_by_xpath(captcha_xpath).get_attribute('data-sitekey')
        captcha_answer = self.captcha_solver(data_sitekey)
        print('typing captcha answer')
        captcha_answer_input_xpath = '//*[@id="g-recaptcha-response"]'
        self.driver.execute_script(
            'document.querySelector("#g-recaptcha-response").style="width: 250px; height: 40px; '
            'border: 1px solid rgb(193, 193, 193); '
            'margin: 10px 25px; padding: 0px; resize: none;"'
        )
        self.driver.find_element_by_xpath(captcha_answer_input_xpath).send_keys(captcha_answer)
        validate_submit = '//*[@class="validate submit"]'
        self.driver.find_element_by_xpath(validate_submit).click()
        sleep(5)

    def tearddown(self):
        self.driver.close()
        sleep(5)
        self.gl.stop()
        sleep(5)
        self.gl.delete(self.profile_id)
        sleep(5)


if __name__ == '__main__':
    while True:
        for index, contact in enumerate(DataBase.df['contact'].dropna().tolist()):
            try:
                sex = Sex24(contact, index)
                sex.spam()
                sex.tearddown()
            except Exception as error:
                LOGGER.exception(error)
