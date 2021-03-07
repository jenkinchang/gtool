from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
import json
import re


def new_driver(pic=True, header=True, path='chromedriver', argument=None):
    """
    :param pic: 是否加载图片
    :param header: 是否以有头模式
    :param path: driver path
    :return: driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument(
        '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81"')
    if pic == False:
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option('prefs', prefs)
    if header == False:
        options.add_argument('--headless')
    if argument:
        options.add_argument(argument)
    driver = webdriver.Chrome(path, options=options)
    driver.maximize_window()
    return driver


def wait_xpath(driver, xpath, s=False, wait_time=10, scroll=True):
    """
    :param driver:
    :param xpath:
    :param s: str or list
    :param wait_time:
    :param scroll: to element
    :return:
    """
    # 清理xpath
    ser_text = re.search(r'/text\(\)$', xpath)
    ser_attribute = re.search(r'/@', xpath)
    text = ''
    attr = ''
    if ser_text:
        xpath = re.sub(r'/text\(\)$', '', xpath)
        text = True
    if ser_attribute:
        attr = re.findall(r'/@(.*)$', xpath)[0]
        xpath = re.sub(r'/@(.*)$', '', xpath)

    # 匹配元素
    def take_value(ele, text, attr):
        if text:
            ele = ele.text
        if attr:
            ele = ele.get_attribute(attr)
        return ele

    try:
        if s == False:
            element = WebDriverWait(driver, wait_time, 0.2).until(
                lambda x: x.find_element_by_xpath(xpath))
            ele_value = take_value(element, text, attr)
            return ele_value
        if s == True:
            elements = WebDriverWait(driver, wait_time, 0.2).until(
                lambda x: x.find_elements_by_xpath(xpath))
            ele_values = [take_value(i, text, attr) for i in elements]
            return ele_values
    except:
        ele_value = None
    finally:
        try:
            if scroll == True:
                scroll_to(driver, element)
        except:
            pass


def scroll_to(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


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
