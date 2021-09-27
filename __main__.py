import itertools
from time import sleep
from os import listdir
from random import choice

from requests import get
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from data import Data
from gologin import GoLogin
from logger import logger

LOGGER = logger('sex24sex')


class Sex24:
    def __init__(self, proxy):
        host, port = proxy.split(':')
        self.gl = GoLogin(dict(token=Data.GOLOGIN_APIKEY))
        self.profile_id = self.gl.create({
            'name': '%s:%s' % (host, port),
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

    def captcha_solver(self, captcha_key):
        print('solving captcha')
        payload = dict(key=Data.RUCAPTCHA_APIKEY,
                       method='userrecaptcha', googlekey=captcha_key, pageurl=Data.URL, json=1)
        req = get('http://rucaptcha.com/in.php', params=payload)
        payload = dict(key=Data.RUCAPTCHA_APIKEY,
                       action='get', id=req.json()['request'], json=1)
        while True:
            req = get('http://rucaptcha.com/res.php', params=payload)
            if req.json()['status']:
                return req.json()['request']

    def upload_photo(self, image_upload):
        images_path = r'C:/Users/KIEV-COP-4/Desktop/images/'
        random_image = images_path + choice([file for file in listdir(images_path) if file.endswith('jpg')])
        self.driver.find_element_by_xpath(image_upload).send_keys(random_image)

    def spam(self, title, detail, contact):
        URL = 'https://1sex24sex.com/add'
        self.driver.get(URL)
        editor_title = '//*[@id="editor_title"]'
        editor = '//*[@id="editor"]'
        contact_xpath = '//*[@name="email"]'
        captcha_xpath = '//*[@id="add-ad-form"]/div[8]'
        captcha_answer_input_xpath = '//*[@id="g-recaptcha-response"]'
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: self.driver.find_element(By.XPATH, editor_title)).send_keys(title)
            self.driver.find_element_by_xpath(editor).send_keys(detail)
            self.driver.find_element_by_xpath(contact_xpath).send_keys(contact)
            image_input = '//*[@id="image-upload-1"]'
            self.upload_photo(image_input)
            data_sitekey = self.driver.find_element_by_xpath(captcha_xpath).get_attribute('data-sitekey')
            captcha_answer = self.captcha_solver(data_sitekey)
            print('typing captcha answer')
            self.driver.execute_script(
                'document.querySelector("#g-recaptcha-response").style="width: 250px; height: 40px; '
                'border: 1px solid rgb(193, 193, 193); '
                'margin: 10px 25px; padding: 0px; resize: none;"'
            )
            self.driver.find_element_by_xpath(captcha_answer_input_xpath).send_keys(captcha_answer)
            validate_submit = '//*[@class="validate submit"]'
            self.driver.find_element_by_xpath(validate_submit).click()
            WebDriverWait(self.driver, 10).until(
                lambda d: self.driver.find_element_by_xpath('//*[@id="second_form"]/div/div[1]/a')).send_keys(title)
            LOGGER.info(f'{contact} {title}')
            return True
        except (TimeoutException, NoSuchElementException) as error:
            LOGGER.error(error)
            return False

    def tearddown(self):
        self.driver.close()
        sleep(2)
        self.gl.stop()
        sleep(2)
        self.gl.delete(self.profile_id)


def main(position):
    title = itertools.cycle(Data('title', position))
    detail = itertools.cycle(Data('detail', position))
    proxy = itertools.cycle(Data('proxy'))
    contact = itertools.cycle(Data('contact'))
    while True:
        sex = Sex24(next(proxy))
        sex.spam(next(title), next(detail), next(contact))
        sex.tearddown()


try:
    if __name__ == '__main__':
        main(629)
except Exception as error:
    LOGGER.exception(error)
