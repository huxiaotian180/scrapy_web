from selenium import webdriver
from lxml import etree
import requests
import json
import sys,base64,hashlib
import time
import requests
import os
from PIL import Image
import image
from API import *
import datetime
from datetime import datetime, date, timedelta
#获取验证码登录验证码
def cutcode_login(count):
    flag = True
    while (flag and count<5):
        try:
            #driver = webdriver.PhantomJS(executable_path="E:\\phantomjs\\bin\\phantomjs.exe")
            driver = webdriver.Chrome()
            #flag = False
            url = 'http://alix.yiche.com/'
            vcodeimgxpath = '//*[@id="img_code"]'
            picName = url.replace(url, "capture.png")
            driver.get(url)
            driver.implicitly_wait(30)
            #driver.maximize_window()
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
            #verifycodeimage.save(os.getcwd() + r'\verifycodeimage.png')
            verifycodeimage.save(r'C:\\python\\verifycodeimage.png')
            count += 1
            #调用验证码接口
            code_text = TestFunc()
            #收到获取验证码
            #print("--------------")
            #code_text = input("输入验证码>>>>")
            # 用户登录
            driver.find_element_by_id('txt_LoginName').send_keys('xxxxxx')
            driver.find_element_by_id('txt_Password').send_keys('xxxxxx@yixin')
            driver.implicitly_wait(30)
            driver.find_element_by_id('txt_Code').send_keys(code_text)
            driver.find_element_by_id('btn_Login').click()
            time.sleep(1)

            # 获取当前系统时间
            timer = str(time.strftime('%Y.%m.%d', time.localtime(time.time()))).split('.')
            time_2 = str(timer[0] + timer[1] + timer[2])
            #获取当前系统前一天时间
            '''
            t = str(date.today() + timedelta(days = -1))
            time_1 = t.split('-')
            time_2 = str(time_1[0] + time_1[1] + time_1[2])
            '''
            #print(t)
            cookies = driver.get_cookies()
            d = list(cookies)
            time.sleep(1)
            alix_server = d[0].get('value')
            JSESSIONID = d[2].get('value')
            global cookie_list
            cookie_list = []
            cookie_list.append(alix_server)
            cookie_list.append(JSESSIONID)
            # 登录成功
            flag = False
            time.sleep(1)
            #print(cookie_list)
            get_data(cookie_list,time_2)


            '''
            iframe_list_1 = []
            iframe1 = driver.find_elements_by_tag_name('iframe')
            for line in iframe1:
                iframe_list_1.append(line.get_attribute('id'))
            print("iframe_list_1:%s" % iframe_list_1)
            time.sleep(1)
            driver.switch_to.frame(driver.find_element_by_id(iframe_list_1[1]))
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="AccordionMenu_leftmenu"]/div[1]/div[1]/div[1]').click()
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="30"]/ul/li[3]/ul/li[7]/div/span[4]').click()
            time.sleep(0.5)
            driver.switch_to.default_content()

            # 获取iframe
            iframe_list_2 = []
            iframe2 = driver.find_elements_by_tag_name('iframe')
            for line in iframe2:
                iframe_list_2.append(line.get_attribute('id'))
            print("iframe_list_2:%s" % iframe_list_2)
            time.sleep(1)
            driver.switch_to.frame(driver.find_element_by_id(iframe_list_2[1]))
            #获取当前系统时间
            time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
            time.sleep(1)

            driver.find_element_by_id('editor_dhtsxqsrq').click()
            driver.find_element_by_id('editor_dhtsxqsrq').send_keys(time)
            driver.find_element_by_id('editor_dhtsxjsrq').click()
            driver.find_element_by_id('editor_dhtsxjsrq').send_keys(time)
            driver.find_element_by_xpath(
                '//*[@id="queryContractForOther_interface_dataset_btnSubmit"]/span/span').click()
            time.sleep(0.5)
            driver.find_element_by_xpath(
                '/html/body/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[2]/table/tbody/tr/td[13]/a/span/span/span').click()
            time.sleep(1)
            driver.find_element_by_id('newWinFramequeryContractForOther').find_element_by_class_name('l-btn-text').click()
            time.sleep(60)
            '''


        except Exception as e:
            print(e)
        finally:
            driver.close()

#识别登录验证码
def identify_code():
    #driver_code = webdriver.PhantomJS(executable_path="E:\\phantomjs\\bin\\phantomjs.exe")
    driver_code = webdriver.Chrome()
    driver_code.maximize_window()
    driver_code.implicitly_wait(30)
    driver_code.get("http://www.fateadm.com/online_identify.html?usr=106335&ukey=YgAAxcNHF5lnR3qLbKQgoSI5swdOGo3e")
    time.sleep(80)
    driver_code.find_element_by_id('pic_type').send_keys('30400')
    time.sleep(1)
    driver_code.find_element_by_id('picFile').send_keys('E:\\web_tsfa\\verifycodeimage.png')
    time.sleep(1)
    driver_code.find_element_by_id('picIdentify').click()
    time.sleep(15)
    page = driver_code.page_source
    time.sleep(1)
    # print(page)
    tree = etree.HTML(page)
    str1 = '//*[@id="msg"]'
    node1 = tree.xpath(str1 + '//text()')
    time.sleep(1)
    global code_text
    code_text = str(node1[1])
    print(code_text)
    driver_code.close()
    return code_text

#获取数据
def get_data(data,ser_time):
    url = "http://alix.yiche.com/trans/qryExp.do"
    payload = "asqbh=&akhxm=&azjlx=&azjh=&dhkrq_f=&dhkrq_t=&atqhkzt=&asqqd=&tsptgsj_f=&tsptgsj_t=&asqdmmc=&asjhm=&azjlxName=&atqhkztName=&asqqdName=&CQId=PrepaymentBackQuery&nextPage=1&everyPage=10&_session_key=dd&databusId=&_dataset_id=PrepaymentBackQuery_dataset&PrepaymentBackQuery_startPage=1&PrepaymentBackQuery_endPage=30&PrepaymentBackQuery_expElements=asqbh%7E2cakhxm%7E2cdhkrq%7E2ctsptgsj%7E2cazjlx%7E2casqqd%7E2catqhklx%7E2casfqz%7E2cazjh%7E2cddqrqsychkr%7E2ciyhqs%7E2ciyqqs%7E2cfkhll%7E2cfzjqk%7E2cftbzj%7E2cfwzfbf%7E2cfwzfgspf%7E2catqhkyj%7E2cdssrq%7E2cassry%7E2casftqhkss%7E2catqhkzt%7E2cassignee%7E2cdhtjqrq%7E2cnormalfsjhkje%7E2casjhm%7E2catbdmc&expType=CSV"
    login_cookie = data
    cookie = ""
    cookie = "alix-server={alix}; JSESSIONID={jession}".format(alix=login_cookie[0], jession=login_cookie[1])
    headers_1 = headers = {
    'host': "alix.yiche.com",
    'connection': "keep-alive",
    'content-length': "657",
    'cache-control': "no-cache",
    'origin': "http://alix.yiche.com",
    'upgrade-insecure-requests': "1",
    'content-type': "application/x-www-form-urlencoded",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'referer': "http://alix.yiche.com/topcars/assets/prepayment/ftl/PrepaymentBackQuery.ftl",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9,und;q=0.8",
    'cookie': cookie
    }

    response = requests.request("POST", url, data=payload, headers=headers_1)
    text = response.text
    #print(text)
    #文件命名规则
    curPath = os.getcwd()
    #tempPath = 'name'
    targetPath = 'X:'
    print(os.path.exists(targetPath))
    if os.path.exists(targetPath):
        print("文件夹存在")
    else:
        os.system("mount \\192.168.1.118\data\windata x:")

    fileName = 'file_advance_' + datetime.now().date().isoformat() + '.txt'
    filePath = targetPath + os.path.sep + fileName

    with open(filePath, 'w', encoding="utf-8") as f_write:
        f_write.write(text)

#积分判断
headers = {'Content-Type': 'application/json;charset=utf-8'}
# api_url = "https://oapi.dingtalk.com/robot/send?access_token=71715565f946e2e2d7b7c0a4b3265647cdcfd940664fd5b9b0837445d88302e4"
api_url = "https://oapi.dingtalk.com/robot/send?access_token=4b4059ce887387a6604a13e345320647d2371678a672a25895a7cbce59698c23"

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


if __name__ == "__main__":
    count = 0
    cutcode_login(count)
    get_jifen()