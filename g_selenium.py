from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
import json


def new_driver(pic=True, header=True, path='chromedriver'):
    """
    :param pic: 是否加载图片
    :param header: 是否以有头模式
    :param path: driver path
    :return: driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66')
    if pic == False:
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option('prefs', prefs)
    if header == False:
        options.add_argument('--headless')
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
            element = take_value(element, text, attr)
        if s == True:
            element = WebDriverWait(driver, wait_time, 0.2).until(
                lambda x: x.find_elements_by_xpath(xpath))
            element = [take_value(i, text, attr) for i in element]
        if scroll == True:
            scroll_to(driver, element)
    except:
        element = None
    return element


def scroll_to(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


def add_cookies(driver, url, cookies):
    if type(cookies) is str:
        cookies = json.loads(cookies)
    driver.get(url)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(url)
    new_cookies = driver.get_cookies()
    return new_cookies

def clean_cookies(cookies):
    for cookie in cookies:
        if 'sameSite' in cookie:
            del cookie['sameSite']
    return cookies