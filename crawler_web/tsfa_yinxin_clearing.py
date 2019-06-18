from selenium import webdriver
from lxml import etree
import time
import requests
import json,re
import os,sys,base64,hashlib
from PIL import Image
import image
import cx_Oracle
from API import *
import datetime
from datetime import datetime, date, timedelta

#获取登陆cookie
def getCookie(select_data,count):
    if len(select_data) != 0:
        flag = True
        while (flag and count<5):
            try:
                # driver = webdriver.PhantomJS(executable_path="E:\\phantomjs\\bin\\phantomjs.exe")
                driver = webdriver.Chrome()
                # flag = False
                url = 'http://alix.yiche.com/'
                vcodeimgxpath = '//*[@id="img_code"]'
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
                count += 1
                code_text = TestFunc()
                # 收到获取验证码
                # print("--------------")
                #code_text = input("输入验证码>>>>")
                # 用户登录
                driver.find_element_by_id('txt_LoginName').send_keys('xxxx')
                driver.find_element_by_id('txt_Password').send_keys('5016xxx841@yixin')
                driver.implicitly_wait(30)
                driver.find_element_by_id('txt_Code').send_keys(code_text)
                driver.find_element_by_id('btn_Login').click()
                time.sleep(1)
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
                #写入文件数据
                f = open(r'X:\\adv_amt.txt', 'w', encoding="utf-8")
                info_text = "申请编号,扣款日期,结清金额\n"
                f.write(info_text)
                for date_info in select_data:
                    print(date_info)
                    data = get_over_info(cookie_list, date_info).strip('"')
                    if len(data) > 0:
                        try:
                            print(date_info, data)
                            curPath = os.getcwd()
                            targetPath = 'X:'
                            print(os.path.exists(targetPath))
                            if os.path.exists(targetPath):
                                print("文件夹存在")
                                string_text = "%s,%s\n" % (date_info,data)
                                f.write(string_text)
                            else:
                                os.system("mount \\192.168.1.118\data\windata x:")

                        except Exception as e:
                            print(e)
                    else:
                        print("文件不存在")

                f.close()


            except Exception as e:
                print(e)
            finally:
                driver.close()
                os.remove(r'X:\\settle_amt.txt')
    else:
        return

#获取数据
def get_over_info(cookie_list,number):
    url = "http://alix.yiche.com/trans/qryExp.do"
    payload = "_dataset_id=OverdueCustomerReceiveMoneyInfo_dataset&_session_key=dd&asqbh=%s&CQId=OverdueCustomerReceiveMoneyInfo&databusId=&everyPage=10&expType=CSV&nextPage=1&OverdueCustomerReceiveMoneyInfo_endPage=30&OverdueCustomerReceiveMoneyInfo_expElements=aSqbh~2ctKkrq~2caKkfs~2caKkzt~2caKkbz~2caKklx~2cfKkje~2caKkfkxx~2caKkhm~2caKkyh~2caKkzh~2caFylx~2caFqxh~2cdZzrq&OverdueCustomerReceiveMoneyInfo_startPage=1" % (number)
    login_cookie = cookie_list
    cookie = ""
    cookie = "alix-server={alix}; JSESSIONID={jession}".format(alix=login_cookie[0], jession=login_cookie[1])
    headers = {
        'host': "alix.yiche.com",
        'connection': "keep-alive",
        'content-length': "433",
        'cache-control': "no-cache",
        'origin': "http://alix.yiche.com",
        'upgrade-insecure-requests': "1",
        'content-type': "application/x-www-form-urlencoded",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'referer': "http://alix.yiche.com/topcars/sales/applyMain/ftl/chargeBackHistory.ftl?asqbh=837609",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9,und;q=0.8",
        'cookie': cookie
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    f = response.text
    file = open("./data.txt", "w", encoding="utf-8")
    file.write(f)
    file.close()
    f = open("./data.txt", encoding="utf-8")
    list = f.readlines()

    # 匹配结清金额
    for line in list:
        regex_str = ".*?([\u4E00-\u9FA5]+结清)"
        match_obj = re.match(regex_str, line)
        if match_obj:
            list_menoy = line.split(',')
            print("匹配金额成功")
            amt = list_menoy[6].strip('"')
            amt_data = list_menoy[1].strip('"')
            amt_str = "%s,%s" % (amt_data, amt)
            return amt_str


#获取查询数据
def select_data():
    """
    host = "117.78.35.224"
    port = "1521"
    sid = "orcl"
    try:
        dsn = cx_Oracle.makedsn(host, port, sid)
        conn = cx_Oracle.connect("odsuser", "f23B7aRk4BW25QJ9", dsn)
        cursor = conn.cursor()
        # select appno from RP_APPLYTONO where appstate in ('6','9') and datatime between to_date('20181226 00:00:00','yyyymmdd hh24:mi:ss') and to_date('20181226 23:59:59','yyyymmdd hh24:mi:ss');
        sql = "select appno from RP_APPLYTONO where appstate in ('6','9') and to_char(datatime,'yyyyMMdd')=to_char(sysdate,'yyyyMMdd')"
        #sql = "select appno from RP_APPLYTONO where appstate in ('6','9') and datatime between to_date('20181226 00:00:00','yyyymmdd hh24:mi:ss') and to_date('20181226 23:59:59','yyyymmdd hh24:mi:ss')"
        cusr = cursor.execute(sql)
        data = list(cusr.fetchall())
        select_data = []
        if len(data) != 0:
            for date in data:
                info = date[0]
                select_data.append(info)
                print("数据查询成功")
        else:
            return
        #db.commit()
        cursor.close()
    except Exception as e:
        print(e)
    finally:
        return select_data
    """
    if os.path.exists(r'X:\\settle_amt.txt'):
        print("文件存在")
        with open(r'X:\\settle_amt.txt') as f:
            content = f.read().split('\n')
            if len(content[-1]) > 0:
                print("ok")
            else:
                del(content[0])
                content.pop(-1)
                return content
    else:
        print("文件不存在")



#插入信息数据
def inster_data(select_data,money):
    """
    host = "117.78.35.224"
    port = "1521"
    sid = "orcl"
    dsn = cx_Oracle.makedsn(host, port, sid)
    conn = cx_Oracle.connect("odsuser", "f23B7aRk4BW25QJ9", dsn)
    cursor = conn.cursor()
    # insert into rp_yx_settleinfo(fp_apply_no,settle_amt) values('1000289075',2332.56);
    #str = "insert into rp_yx_settleinfo(fp_apply_no,settle_amt) values('%s','%s')"
    sql = "insert into rp_yx_settleinfo(fp_apply_no,settle_amt) values('%s','%s')" % (select_data,money)
    cusr = cursor.execute(sql)
    conn.commit()
    print("数据库插入成功")
    cursor.close()
    """



#积分判断
headers = {'Content-Type': 'application/json;charset=utf-8'}
#api_url = "https://oapi.dingtalk.com/robot/send?access_token=71715565f946e2e2d7b7c0a4b3265647cdcfd940664fd5b9b0837445d88302e4"
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
    data_info = select_data()
    if data_info is None:
        print("无可用数据")
    else:
        getCookie(data_info, count)
        get_jifen()
