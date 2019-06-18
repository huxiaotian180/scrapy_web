import requests,hashlib,os,sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time,datetime,os,sqlite3,json,ssl
from win32.win32crypt import CryptUnprotectData
from win32.win32crypt import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


def login():
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)  # seconds
    browser.get('http://yun.yxqiche.com')  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
    # 登陆
    browser.find_element_by_id("username").send_keys('xxxx')
    browser.find_element_by_id("password").send_keys('xxxxxx@yixin')
    browser.find_element_by_class_name("btn-submit").click()
    browser.maximize_window()
    time.sleep(2)
    # 进入贷后页面
    browser.find_element_by_class_name("imgDiv").click()
    time.sleep(120)
    browser.close()

if __name__ == "__main__":
    login()