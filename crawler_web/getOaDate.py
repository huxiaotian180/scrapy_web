import requests,hashlib,os,sys,image
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time,datetime,os,sqlite3,json,ssl
from PIL import Image
from win32.win32crypt import CryptUnprotectData
from win32.win32crypt import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from API import *

#用户登陆

def login(count):
    flag = True
    while count<5:
        try:
            url = "http://yun.yxqiche.com"
            browser = webdriver.Chrome()
            browser.implicitly_wait(10)  # seconds
            browser.get(url)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
            cookies_open = browser.get_cookie("JSESSIONID")["value"]
            # print(cookies_open)

            # 验证码识别
            vcodeimgxpath = '//*[@id="codeimg"]'
            picName = url.replace(url, "capture_oa.png")
            time.sleep(1)
            browser.save_screenshot(picName)
            time.sleep(1)

            imgelement = browser.find_element_by_xpath(vcodeimgxpath)
            location = imgelement.location
            size = imgelement.size
            rangle = (int(location['x']),
                      int(location['y']),
                      int(location['x'] + size['width']),
                      int(location['y'] + size['height']))
            i = Image.open(os.getcwd() + r'\capture_oa.png')
            verifycodeimage = i.crop(rangle)
            # verifycodeimage.save(os.getcwd() + r'\verifycodeimage.png')
            verifycodeimage.save(r'C:\\python\\verifycodeimage.png')

            count = count + 1
            code_text = TestFunc()
            print(code_text)

            # 登陆
            browser.find_element_by_id("username").send_keys('xxxxxxx')
            browser.find_element_by_id("password").send_keys('sssss@yixin')
            browser.find_element_by_id("imageCode").send_keys(code_text)
            browser.find_element_by_class_name("btn-submit").click()
            cookies_login = browser.get_cookie("SESSION")["value"]
            # print(cookies_login)

            time.sleep(2)
            # 进入贷后页面
            browser.find_element_by_class_name("imgDiv").click()
            cookies_oa = browser.get_cookies()

            # 加入cookies登陆
            browser.add_cookie({'name': "JSESSIONID", 'value': cookies_open})
            browser.add_cookie({'name': "SESSION", 'value': cookies_login})

            browser.get("https://oacas.yixincapital.com/casserver/login?service=https://finaloan-web.yixincapital.com/finaloan-web/shiro-cas")
            time.sleep(1)
            #登陆成功
            flag = False
            cookies_user = browser.get_cookie("JSESSIONID")["value"]
            cookies_user_name = "JSESSIONID={cookies}".format(cookies=cookies_user)
            # print("cookies_user:%s"%cookies_user)
            get_yixin_data(cookies_user_name)
        except Exception as e:
            print(e)
        finally:
            browser.close()



#获取cookies
def getcookiefromchrome(host='finaloan-web.yixincapital.com'):
    flag = True
    while flag:
        try:
            cookiepath = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"
            sql = "select host_key,name,encrypted_value from cookies where host_key='%s'" % host
            with sqlite3.connect(cookiepath) as conn:
                cu = conn.cursor()
                cookies = {name: CryptUnprotectData(encrypted_value)[1].decode() for host_key, name, encrypted_value in
                           cu.execute(sql).fetchall()}
                if len(cookies) > 0:
                    flag = False
                else:
                    print("未获取cookies")
                    time.sleep(60)
                    login()
        except Exception as e:
            print("连接数据库失败")
    return cookies

#获取查询数据
def select_data():
    if not os.path.exists(r'X:\\yx_oa_repay.txt'):
        sys.exit(0)

    with open(r'X:\\yx_oa_repay.txt') as f:
        content = f.read().split('\n')
        if  len(content) <= 0:
            sys.exit(0)

        del(content[0])
        return content



#报文数据签名
def md5_sing(applyNo):
    # md5加密
    m = hashlib.md5()
    md5text = "applyNo=%sbusinessType=certNo=current=1custName=custPhone=endTime=feeType=rowCount=10startTime=status=" % applyNo
    m.update(md5text.encode("utf-8"))
    return m.hexdigest()

#数据查询
def select_requests(md5_text,cookies,applyNo):
    url = "https://finaloan-web.yixincapital.com/finaloan-web/preRepay/queryWithholdingPageInfo.do"
    payload = "applyNo=%s&custName=&certNo=&custPhone=&startTime=&endTime=&status=&businessType=&feeType=&current=1&rowCount=10" % applyNo
    headers = {
        'Host':"finaloan-web.yixincapital.com",
        'Connection':"keep-alive",
        'Content-Length':"120",
        'Accept':"application/json, text/plain, */*",
        'Origin':"https://finaloan-web.yixincapital.com",
        'yixin':md5_text,
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
        'Content-Type':"application/x-www-form-urlencoded",
        'Referer':"https://finaloan-web.yixincapital.com/finaloan-web/finaloan-vue/repayment/index.html",
        'Accept-Encoding':"gzip, deflate, br",
        'Accept-Language':"zh-CN,zh;q=0.9,und;q=0.8",
        'Cookie':cookies,
        'cache-control':"no-cache"
    }
    #print(headers)
    #print(payload)
    response = requests.request("POST", url, data=payload, headers=headers, verify=False)
    return response

#获取数据
def get_yixin_data(cookies):
    # 准备写入文件数据
    targetPath = 'X:'
    print(os.path.exists(targetPath))
    if os.path.exists(targetPath):
        f = open(r'X:\\OA_message.txt', 'w', encoding="utf-8")
        info_text = "申请号,证件号,扣款日期,费用类型,账单日期,扣款方式,扣款金额,扣款户名,扣款银行,扣款账号,扣款状态\n"
        f.write(info_text)
    else:
        os.system("mount \\192.168.1.118\data\windata x:")

    #获取查询数据信息列表
    list_data = select_data()
    print(list_data)
    if len(list_data) <= 0:
        sys.exit(0)
    for line in list_data:
        if len(line) <= 0:
            f.close()
            sys.exit(0)
        # 获取签名
        md5_text = md5_sing(line)
        #获取数据
        response = select_requests(md5_text, cookies,line)
        print(response)
        try:
            data_text = response.json()
            text_message = data_text["data"]
            print(len(text_message))
            if len(text_message) > 0:
                for data in text_message:
                    info_message = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (
                        data["applyNo"],
                        data["idCard"],
                        data["completeTime"],
                        data["remark"],
                        data["planRepayDate"],
                        data["paymentChannel"],
                        data["amount"],
                        data["accountName"],
                        data["cnName"],
                        data["accountNo"],
                        data["status"])
                    print(info_message)
                    f.write(info_message)
            else:
                print("数据为空")

        except Exception as e:
            print("返回内容错误")
    print("数据爬虫结束")
if __name__ =="__main__":
    login(count=1)



