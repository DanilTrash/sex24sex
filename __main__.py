import itertools
from os import listdir
from random import choice
from time import sleep

from requests import get
from selenium.webdriver import Remote
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from data import Data
from logger import logger

LOGGER = logger('sex24sex')


class Sex24:
    def __init__(self, profile_id) -> None:
        self.profile_id = profile_id
        mla_url = 'http://127.0.0.1:35000/api/v1/profile/start?automation=true&profileId=' + self.profile_id
        self.resp = get(mla_url).json()
        if self.resp['status'] == 'OK':
            value = self.resp['value']
            self.driver = Remote(command_executor=value, desired_capabilities={'acceptSslCerts': True})
        elif self.resp['status'] == 'ERROR':
            get('http://127.0.0.1:35000/api/v1/profile/stop?automation=true&profileId=' + self.profile_id)

    def captcha_solver(self, captcha_key) -> str:
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

    def upload_photo(self) -> None:
        image_input = '//*[@id="image-upload-1"]'
        images_path = r'C:/Users/KIEV-COP-4/Desktop/images/'
        random_image = images_path + choice([file for file in listdir(images_path) if file.endswith('jpg')])
        try:
            self.driver.find_element_by_xpath(image_input).send_keys(random_image)
        except NoSuchElementException as error:
            LOGGER.error(error)

    def spam(self, title, detail, contact) -> bool:
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
            # self.upload_photo(image_input)
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
                lambda d: self.driver.find_element_by_xpath('//*[@id="second_form"]/div/div[1]/a'))
            LOGGER.info(f'{contact} {title}')
            return True
        except (TimeoutException, NoSuchElementException) as error:
            LOGGER.error(error)
            return False

    def tearddown(self):
        self.driver.quit()


def main(position=0):
    title = itertools.cycle(Data('title', position))
    detail = itertools.cycle(Data('detail', position))
    profiles = itertools.cycle(Data('profile'))
    contact = itertools.cycle(Data('contact'))
    for profile in profiles:
        sex = Sex24(profile)
        sex.spam(next(title), next(detail), next(contact))
        sex.tearddown()
        sleep(60*30)


try:
    if __name__ == '__main__':
        main()
except Exception as error:
    LOGGER.exception(error)
