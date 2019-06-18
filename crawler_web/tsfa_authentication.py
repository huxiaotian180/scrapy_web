import json
from selenium import webdriver
from lxml import etree
import time
import requests
import json
import os,sys,base64,hashlib
from PIL import Image
import image
from API import *
import datetime
from datetime import datetime, date, timedelta
import re

#钉钉接口地址
headers = {'Content-Type': 'application/json;charset=utf-8'}
api_url = "https://oapi.dingtalk.com/robot/send?access_token=4b4059ce887387a6604a13e345320647d2371678a672a25895a7cbce59698c23"
def tsfa_auth(jifen,count,falge,data):
    if  jifen>=10:
        while (count < 10):
            try:
                # driver = webdriver.PhantomJS(executable_path="E:\\phantomjs\\bin\\phantomjs.exe")
                driver = webdriver.Chrome()
                # flag = False
                url = data[0]
                vcodeimgxpath = data[1]
                picName = url.replace(url, "capture.png")
                driver.get(url)
                driver.implicitly_wait(30)
                # driver.maximize_window()
                time.sleep(1)
                driver.save_screenshot(picName)
                time.sleep(3)

                imgelement = driver.find_element_by_xpath(vcodeimgxpath)
                location = imgelement.location
                size = imgelement.size
                rangle = (int(location['x']),
                          int(location['y']),
                          int(location['x'] + size['width']),
                          int(location['y'] + size['height']))
                i = Image.open(os.getcwd() + r'\capture.png')
                verifycodeimage = i.crop(rangle)
                # verifycodeimage.save(os.getcwd() + r'\verifycodeimage.png')
                verifycodeimage.save(r'C:\\python\\verifycodeimage.png')
                # 调用验证码接口
                count = count + 1
                code_text = TestFunc()
                # 调用验证码接口
                #code_text = TestFunc()
                # code_text = input("输入验证码>>>>")
                # 用户登录
                driver.find_element_by_name('userName').send_keys(data[2])
                driver.find_element_by_name('passWord').send_keys(data[3])
                driver.implicitly_wait(30)
                driver.find_element_by_id('txt_Code').send_keys(code_text)
                driver.find_element_by_id('btn_Login').click()
                time.sleep(1)
                driver.switch_to.frame(driver.find_element_by_id('leftmenu'))
                falge = True
                if falge:
                    text = "登陆成功:" + url
                    msg(text)
                    #print(text)
                break

            except Exception as e:
                print(e)
                if count == 10:
                    text = "登陆失败:" + url
                    msg(text)
                    #print(text)
            finally:
                driver.close()

#积分判断,登陆接口判断
def msg(text):
    json_text = {
        "msgtype": "text",
        "at": {
            "isAtAll": False
        },
        "text": {
            "content": text
        }
    }
    requests.post(api_url, json.dumps(json_text), headers=headers)

def CalcSign(usr_id, passwd, timestamp):
    md5     = hashlib.md5();
    md5.update((timestamp + passwd).encode());
    csign   = md5.hexdigest();

    md5     = hashlib.md5();
    md5.update((usr_id + timestamp + csign).encode());
    csign   = md5.hexdigest();
    return csign;

def HttpRequest(url, body_data):
    #rsp         = Rsp();
    post_data   = body_data;
    header      = {
            'User-Agent': 'Mozilla/5.0',
            };
    rsp_data    = requests.post(url, post_data, headers=header);
    return rsp_data.text

def get_jifen():
    tm = str(int(time.time()));
    usr_id='106335'
    usr_key='YgAAxcNHF5lnR3qLbKQgoSI5swdOGo3e'
    sign = CalcSign(usr_id,usr_key, tm);
    param = {
        "user_id": usr_id,
        "timestamp": tm,
        "sign": sign
    };
    host= 'http://pred.fateadm.com'
    url = host + "/api/custval"
    rsp = HttpRequest(url, param)

    text = json.loads(json.loads(rsp)['RspData'])['cust_val']
    if text < 50:
        message = '验证码接口积分小于50，请尽快充值！！！'
        msg(message)

    return text



if __name__=="__main__":
    jifen = get_jifen()
    login_data = [("http://wl.baixin.net.cn/alix/", "//*[@id=\"img_code\"]", "xxxxx", "xxxxxxxx@888888"),
            ("http://chedai.baixin.net.cn/blix/", "//*[@id=\"oimg\"]", "xxxxx", "xxxxxx@888888"),
            ("http://chedai.cherrydai.com/dlix/", "//*[@id=\"oimg\"]", "xxxxx", "xxxxx@888888")
            ]
    for line in range(0, login_data.__len__()):
        falge = False
        count=0
        tsfa_auth(jifen,count,falge,login_data[line])

    #会员积分判断

