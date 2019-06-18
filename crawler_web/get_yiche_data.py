from selenium import webdriver
from lxml import etree
import time
import requests
import os,sys
import base64
import hashlib
import json
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
            #调用验证码接口
            count += 1
            code_text = TestFunc()
            #收到获取验证码
            #print("--------------")
            #code_text = input("输入验证码>>>>")
            # 用户登录  账号：kehufuli；密码：5016841@yixin
            driver.find_element_by_id('txt_LoginName').send_keys('xxxxxx')
            driver.find_element_by_id('txt_Password').send_keys('5016841@yixin')
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
    payload = "contractno=&productversion=&versionSrt=&asqbh=&apzsx=&acllx=&acpfa=&akhxm=&azjhm=&asqzt=&ahtzt=&dsqqsrq=&dsqjsrq=&aqydm=&apqdm=&afgsdm=&azlgsdm=&atbddmName=&dhtjqqsrq=&dhtjqjsrq=&asfrbx=&agpsjglx=&ahxhm=&aywlx=&ssp_id=&sfzxdzf=&asfbtc=&akhqdlx=&arzqx=&acphm=&akhqd1=&akhqd2=&ahzqd1=&ahzqd2=&ywgsName=&ywgsName=&ywgs=&apzsxName=&acllxName=&asqztName=&ahtztName=&aqydmName=&apqdmName=&afgsdmName=&azlgsdmName=&asfrbxName=&agpsjglxName=&aywlxName=&ssp_idName=&sfzxdzfName=&asfbtcName=&akhqdlxName=&arzqxName=&akhqd1Name=&akhqd2Name=&ahzqd1Name=&ahzqd2Name=&ywgsNameName=&CQId=queryContractDayReport&nextPage=1&everyPage=10&_session_key=dd&databusId=&queryContractDayReport=queryContractDayReport&_dataset_id=queryContractDayReport_dataset&queryContractDayReport_startPage=1&queryContractDayReport_endPage=30&queryContractDayReport_expElements=opr%257E2chistory%257E2casqbh%257E2ccontractno%257E2casqlx%257E2cssp%257E5fid%257E2ccapital%257E5fcode%257E5fafter%257E2cayhxszt%257E2cakhxm%257E2casqrxb%257E2cayhzk%257E2canl%257E2cadwmc%257E2cagddh%257E2cadwszsfname%257E2cadwszcsName%257E2cadwxxdz%257E2cazjlx%257E2cazjhm%257E2cacllx%257E2capzsx%257E2carzqx%257E2cacpfamc%257E2casfrbx%257E2cdsqrq%257E2casqzt%257E2cadmsx%257E2cazcs%257E2capp%257E2cacxi%257E2cacx%257E2cfxsj%257E2cacjh%257E2cfxczdj%257E2casfwc%257E2caclqdmc%257E2caclkpdw%257E2cloanTime%257E2cafdjh%257E2caclys%257E2cacphm%257E2catzgw%257E2cfrze%257E2cffxrze%257E2cffxrze2%257E2cfkhll%257E2cfjsll%257E2casfbl%257E2cfsfje%257E2cawfbl%257E2cawfk%257E2cfsxfl%257E2cfsxf%257E2cfjssxfl%257E2cfbtsxf%257E2cfbzjbl%257E2cfbzj%257E2cfmqkhzj%257E2cahtcjrq%257E2cdhtsxrq%257E2cahtjsrq%257E2catbddm%257E2catbddmName%257E2cadmsfName%257E2cadmcsName%257E2cazypp%257E2cadq%257E2capq%257E2cafgs%257E2cassgs%257E2caxsgw%257E2caposjhm%257E2casjhm%257E2cakhrkhh%257E2cahkrjjkzh%257E2cahkrkhm%257E2cdyjhkr%257E2casfrz%257E2cbf%257E2cfwydqxbf%257E2cfbtbl%257E2cftxze%257E2cgzs%257E2cfccs%257E2cfsyxbf%257E2cfjqxbf%257E2cabxgsmc%257E2cgpsyjazf%257E2cgpsbaseprice%257E2cgpsaddprice%257E2cgpsfwf%257E2cxcfprq%257E2cacpsssf%257E2cacpsscs%257E2cagpssfan%257E2cagpssfrz%257E2casimkh1%257E2casimkh2%257E2cfjzje%257E2cfybje%257E2cdhtfkrq%257E2cakhly%257E2cakhqdlx%257E2cagpsjglx%257E2cchannel%257E2cdwzt%257E2cclientsource%257E2cbranchname%257E2csalesname%257E2cacplb%257E2cazcblx%257E2cffke%257E2cgpstype%257E2cadmdz%257E2cfsybj%257E2cfkhrzje%257E2csfzxdzf%257E2cfukuantype%257E2cafpfgs%257E2ctbrzh%257E2ctbrmc%257E2caskfmc%257E2caskfyh%257E2caskfzh%257E2cchannelname%257E2casxfkkfsName%257E2cbzjcd%257E2caywlx%257E2cfcstxze%257E2cfdlstxze%257E2cappraisalprice%257E2caywgs%257E2cgpspaystatus%257E2caglddh%257E2czhglf%257E2cffccs%257E2cffsyxbf%257E2cffjqxbf%257E2cfbf%257E2cacgj%257E2ccgjgysmc%257E2cversionSrt%257E2casfbtc%257E2cafqdsxf%257E2cyhfkzt%257E2cajxsjc%26expType%3ACSV"
    login_cookie = data
    cookie = ""
    cookie = "alix-server={alix}; JSESSIONID={jession}".format(alix=login_cookie[0], jession=login_cookie[1])
    print(cookie)
    #payload = "contractno=&asqbh=&dhtsxqsrq={star_time}&dhtsxjsrq={end_time}&apzsx=&acllx=&acpfa=&akhxm=&azjhm=&ahtzt=&dsqqsrq=&dsqjsrq=&asqzt=&aqydm=&apqdm=&afgsdm=&azlgsdm=&atbddmName=&dhtjqqsrq=&agpsjglx=&ahxhm=&aywlx=&akhqdlx=&arzqx=&dhtjqjsrq=&asfrbx=&akhqd1=&akhqd2=&ahzqd1=&ahzqd2=&apzsxName=&acllxName=&ahtztName=&asqztName=&aqydmName=&apqdmName=&afgsdmName=&azlgsdmName=&agpsjglxName=&aywlxName=&akhqdlxName=&arzqxName=&asfrbxName=&akhqd1Name=&akhqd2Name=&ahzqd1Name=&ahzqd2Name=&CQId=queryContractForOther&nextPage=1&everyPage=10&_session_key=dd&databusId=&queryContract=queryContract&_dataset_id=queryContractForOther_dataset&queryContractForOther_startPage=1&queryContractForOther_endPage=30&queryContractForOther_expElements=opr~2chistory~2casqbh~2ccontractno~2casqlx~2cakhxm~2casqrxb~2cayhzk~2canl~2cadwmc~2cagddh~2cadwszsfname~2cadwszcsName~2cadwxxdz~2cazjlx~2cazjhm~2cacllx~2capzsx~2carzqx~2cacpfamc~2casfrbx~2cdsqrq~2casqzt~2cadmsx~2cazcs~2capp~2cacxi~2cacx~2cfxsj~2cacjh~2cfxczdj~2casfwc~2caclqdmc~2caclkpdw~2cafdjh~2caclys~2cacphm~2catzgw~2cfrze~2cffxrze~2cffxrze2~2cfkhll~2cfjsll~2casfbl~2cfsfje~2cawfbl~2cawfk~2cfsxfl~2cfsxf~2cfjssxfl~2cfbtsxf~2cfbzjbl~2cfbzj~2cfmqkhzj~2cahtcjrq~2cdhtsxrq~2cahtjsrq~2catbddm~2catbddmName~2cadmsfName~2cadmcsName~2cazypp~2cadq~2capq~2cafgs~2cassgs~2caxsgw~2caposjhm~2casjhm~2cakhrkhh~2cahkrjjkzh~2cahkrkhm~2cdyjhkr~2casfrz~2cbf~2cfwydqxbf~2cfbtbl~2cftxze~2cgzs~2cfccs~2cfsyxbf~2cfjqxbf~2cabxgsmc~2cgpsyjazf~2cgpsfwf~2cxcfprq~2cacpsssf~2cacpsscs~2cagpssfan~2cagpssfrz~2casimkh1~2casimkh2~2cfjzje~2cfybje~2cdhtfkrq~2cakhqdlx~2cagpsjglx~2cchannel~2cdwzt~2cclientsource~2cbranchname~2csalesname~2cacplb~2cazcblx~2cffke~2cgpstype~2cfzhglf~2caczry~2cfzxbje~2cfsybj&expType=CSV".format(star_time=ser_time,end_time=ser_time)

    payload = "contractno=&productversion=&versionSrt=&asqbh=&apzsx=&acllx=&acpfa=&akhxm=&azjhm=&asqzt=&ahtzt=&dsqqsrq=&dsqjsrq=&aqydm=&apqdm=&afgsdm=&azlgsdm=&atbddmName=&dhtjqqsrq=&dhtjqjsrq=&asfrbx=&agpsjglx=&ahxhm=&aywlx=&ssp_id=&sfzxdzf=&asfbtc=&akhqdlx=&arzqx=&acphm=&akhqd1=&akhqd2=&ahzqd1=&ahzqd2=&ywgsName=&ywgsName=&ywgs=&apzsxName=&acllxName=&asqztName=&ahtztName=&aqydmName=&apqdmName=&afgsdmName=&azlgsdmName=&asfrbxName=&agpsjglxName=&aywlxName=&ssp_idName=&sfzxdzfName=&asfbtcName=&akhqdlxName=&arzqxName=&akhqd1Name=&akhqd2Name=&ahzqd1Name=&ahzqd2Name=&ywgsNameName=&CQId=queryContractDayReport&nextPage=1&everyPage=10&_session_key=dd&databusId=&queryContractDayReport=queryContractDayReport&_dataset_id=queryContractDayReport_dataset&queryContractDayReport_startPage=1&queryContractDayReport_endPage=30&queryContractDayReport_expElements=opr~2chistory~2casqbh~2ccontractno~2casqlx~2cssp~5fid~2ccapital~5fcode~5fafter~2cayhxszt~2cakhxm~2casqrxb~2cayhzk~2canl~2cadwmc~2cagddh~2cadwszsfname~2cadwszcsName~2cadwxxdz~2cazjlx~2cazjhm~2cacllx~2capzsx~2carzqx~2cacpfamc~2casfrbx~2cdsqrq~2casqzt~2cadmsx~2cazcs~2capp~2cacxi~2cacx~2cfxsj~2cacjh~2cfxczdj~2casfwc~2caclqdmc~2caclkpdw~2cloanTime~2cafdjh~2caclys~2cacphm~2catzgw~2cfrze~2cffxrze~2cffxrze2~2cfkhll~2cfjsll~2casfbl~2cfsfje~2cawfbl~2cawfk~2cfsxfl~2cfsxf~2cfjssxfl~2cfbtsxf~2cfbzjbl~2cfbzj~2cfmqkhzj~2cahtcjrq~2cdhtsxrq~2cahtjsrq~2catbddm~2catbddmName~2cadmsfName~2cadmcsName~2cazypp~2cadq~2capq~2cafgs~2cassgs~2caxsgw~2caposjhm~2casjhm~2cakhrkhh~2cahkrjjkzh~2cahkrkhm~2cdyjhkr~2casfrz~2cbf~2cfwydqxbf~2cfbtbl~2cftxze~2cgzs~2cfccs~2cfsyxbf~2cfjqxbf~2cabxgsmc~2cgpsyjazf~2cgpsbaseprice~2cgpsaddprice~2cgpsfwf~2cxcfprq~2cacpsssf~2cacpsscs~2cagpssfan~2cagpssfrz~2casimkh1~2casimkh2~2cfjzje~2cfybje~2cdhtfkrq~2cakhly~2cakhqdlx~2cagpsjglx~2cchannel~2cdwzt~2cclientsource~2cbranchname~2csalesname~2cacplb~2cazcblx~2cffke~2cgpstype~2cadmdz~2cfsybj~2cfkhrzje~2csfzxdzf~2cfukuantype~2cafpfgs~2ctbrzh~2ctbrmc~2caskfmc~2caskfyh~2caskfzh~2cchannelname~2casxfkkfsName~2cbzjcd~2caywlx~2cfcstxze~2cfdlstxze~2cappraisalprice~2caywgs~2cgpspaystatus~2caglddh~2czhglf~2cffccs~2cffsyxbf~2cffjqxbf~2cfbf~2cacgj~2ccgjgysmc~2cversionSrt~2casfbtc~2cafqdsxf~2cyhfkzt~2cajxsjc&expType=CSV"
    headers = {
        'host': "alix.yiche.com",
        'connection': "keep-alive",
        'content-length': "2508",
        'cache-control': "no-cache",
        'origin': "http://alix.yiche.com",
        'upgrade-insecure-requests': "1",
        'content-type': "application/x-www-form-urlencoded",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'referer': "http://alix.yiche.com/topcars/sales/applyMain/ftl/queryContractReportDay.ftl",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9,und;q=0.8",
        'cookie':cookie
    }

    response = requests.request("POST", url, data=payload, headers=headers)
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

    fileName = 'file_toappno_' + datetime.now().date().isoformat() + '.txt'
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
    #time.sleep(50000)



