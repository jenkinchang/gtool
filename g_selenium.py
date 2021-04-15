from selenium.webdriver.support.wait import WebDriverWait
from types import MethodType
from requestium import Session, Keys
import json
import re
from lxml import etree

from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from types import MethodType
from requestium import Session
import json
import re
from lxml import etree


def new_session(pic=True, header=True, path='chromedriver', argument=None):
    """
    :param pic: 是否加载图片
    :param header: 是否以有头模式
    :param path: driver path
    :return: driver
    """

    def _get(self, url):
        self.get(url)
        return self

    def xpath(self, xpath, type='all'):
        # clean
        if re.search(r'/text\(\)$', xpath):
            f_xpath = re.sub(r'/text\(\)$', '', xpath)
        elif re.search(r'/@', xpath):
            f_xpath = re.sub(r'/@.*$', '', xpath)
        else:
            f_xpath = xpath
        # wait
        if type == 'first':
            WebDriverWait(self, 5, 0.2).until(
                lambda x: x.find_element_by_xpath(f_xpath))
        elif type == 'all':
            WebDriverWait(self, 5, 0.2).until(
                lambda x: x.find_elements_by_xpath(f_xpath))
        else:
            raise
        # xpath
        html = self.page_source
        element = etree.HTML(html).xpath(xpath)
        return element

    def go_to(self, element):
        self.execute_script("arguments[0].scrollIntoView();", element)

    def execjs(self, js_text):
        return self.execute_script(js_text)

    options = {
        'arguments': [
            '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81"']
    }

    #     if pic == False:
    #         prefs = {"profile.managed_default_content_settings.images": 2}
    #         options['add_experimental_option']  = ['prefs', prefs]
    if header == False:
        options['arguments'].append('--headless')
    if argument:
        options['arguments'].append(argument)

    s = Session(
        webdriver_path='chromedriver',
        browser='chrome',
        webdriver_options=options
    )

    s.driver._get = MethodType(_get, s.driver)
    s.driver.xpath = MethodType(xpath, s.driver)
    s.driver.go_to = MethodType(go_to, s.driver)
    s.driver.execjs = MethodType(execjs, s.driver)

    # s.proxies.update({
    #     "http": None,
    #     "https": None,
    # })

    return s


# use s.driver.ensure_add_cookie
def add_cookies(driver, url, cookies):
    if type(cookies) is str:
        cookies = json.loads(cookies)
    driver.get(url)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(url)
    driver.refresh()
    new_cookies = driver.get_cookies()
    return new_cookies


def clean_cookies(cookies):
    for cookie in cookies:
        if 'sameSite' in cookie:
            del cookie['sameSite']
    return cookies
