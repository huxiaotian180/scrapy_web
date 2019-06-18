import requests,hashlib,os,sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time,datetime,os,sqlite3,json,ssl
from win32.win32crypt import CryptUnprotectData
from win32.win32crypt import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from API import *
from PIL import Image


#用户登陆
def login(count):
    flag = True

    while count < 3 and flag:
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
            # 识别验证码
            code_text = TestFunc()
            print(code_text)
            # code_text = input()

            # 登陆kehufuli/5016841@yixin
            browser.find_element_by_id("username").send_keys('zxxxxxx')
            browser.find_element_by_id("password").send_keys('xxxxxx@yixin')
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

            browser.get(
                "https://oacas.yixincapital.com/casserver/login?service=https://finaloan-web.yixincapital.com/finaloan-web/shiro-cas")
            time.sleep(1)
            # 登陆成功
            cookies_user = browser.get_cookie("JSESSIONID")["value"]
            cookies_user_name = "JSESSIONID={cookies}".format(cookies=cookies_user)
            # print("cookies_user:%s"%cookies_user)
            # 正常提前还款结清
            settle_data(cookies_user_name, '01')
            # 开始爬取提前结清数据
            settle_data(cookies_user_name, '02')
            # 开始爬取强制提前结清数据
            settle_data(cookies_user_name, '06')
            flag = False
        except Exception as e:
            flag = True
            print(e)
        finally:
            browser.close()


# 获取cookies
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
                print(cookies)
                if len(cookies) > 0:
                    flag = False
                else:
                    time.sleep(60)
                    login()
        except Exception as e:
            print("连接数据库失败")

    return cookies


# 报文数据签名
def md5_sing(settleDateStart, settleDateEnd, settleType):
    # md5加密
    print('md5加密')
    m = hashlib.md5()
    md5text = "applyId=current=1custName=dataSource=overdueLevel=productName=repayDate=repayStatus=repurchased=rowCount=10serviceType=settleDateEnd=%ssettleDateStart=%ssettleType=%svehicleFrameNum=" % (settleDateEnd, settleDateStart, settleType)
    m.update(md5text.encode("utf-8"))
    return m.hexdigest()


# 爬取结清数据
def select_settle(md5_text, cookies, settleDateStart, settleDateEnd, settleType):
    url = "https://finaloan-web.yixincapital.com/finaloan-web/lloanApply/query.do"
    payload = "current=1&rowCount=10&settleDateStart=%s&settleDateEnd=%s&serviceType=&applyId=&custName=&productName=&repayStatus=&repayDate=&settleType=%s&dataSource=&overdueLevel=&vehicleFrameNum=&repurchased=" % (settleDateStart, settleDateEnd, settleType)
    headers = {
        'Host': "finaloan-web.yixincapital.com",
        'Connection': "keep-alive",
        'Content-Length': "18",
        'Accept': "application/json, text/plain, */*",
        'Origin': "https://finaloan-web.yixincapital.com",
        'yixin': md5_text,
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
        'Content-Type': "application/x-www-form-urlencoded",
        'Referer': "https://finaloan-web.yixincapital.com/finaloan-web/finaloan-vue/repayment/index.html?_rp-480452431=-480452431",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9,und;q=0.8",
        'Cookie': cookies,
        'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=payload, headers=headers, verify=False)
    return response


# 获取数据
def settle_data(cookies, settleType):
    # 准备写入文件数据
    print('cookies:', cookies)
    targetPath = 'x:/yx/settle'
    print(os.path.exists(targetPath))
    today = datetime.date.today()
    print("日期:", today)
    if os.path.exists(targetPath):
        f = open(r'x:/yx/settle/settle.txt', 'w', encoding="utf-8")
        info_text = "申请号,客户姓名,业务类型,产品名称,贷款金额,车架号,结清类型,结清日期\n"
        f.write(info_text)
        print("开始写入文件:", today)
    else:
        os.system("mount \\192.168.1.118\data\windata x:")

    # 获取提前结清数据
    # 获取签名
    md5_text = md5_sing(today, today, settleType)
    # cc1b5cf4ff308ca97d82cd8c2fcdbf42
    print('md5_text:', md5_text)
    response = select_settle(md5_text, cookies, today, today, settleType)
    print(response)
    try:
        data_text = response.json()
        # print(data_text)
        text_message = data_text["data"]["data"]
        # print(len(text_message))
        if len(text_message) > 0:
            for data in text_message:
                info_message = "%s,%s,%s,%s,%s,%s,%s,%s\n" % (
                    data["applyId"],
                    data["custName"],
                    data["serviceTypeName"],
                    data["productName"],
                    data["loanAmount"],
                    data["vehicleFrameNum"],
                    data["settleStatusName"],
                    data["settleDate"])
                print(info_message)
                f.write(info_message)
        else:
            print("数据为空")

    except Exception as e:
        print("返回内容错误")
    print("数据爬虫结束")


if __name__ =="__main__":
    login(count=1)



