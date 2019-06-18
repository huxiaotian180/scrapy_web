import os
import time
import datetime
from datetime import datetime, date, timedelta
import cx_Oracle
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
#获取验证码登录验证码



def get_over_info(number):
    url = "http://alix.yiche.com/trans/qryExp.do"
    payload = "_dataset_id=OverdueCustomerReceiveMoneyInfo_dataset&_session_key=dd&asqbh=%s&CQId=OverdueCustomerReceiveMoneyInfo&databusId=&everyPage=10&expType=CSV&nextPage=1&OverdueCustomerReceiveMoneyInfo_endPage=30&OverdueCustomerReceiveMoneyInfo_expElements=aSqbh~2ctKkrq~2caKkfs~2caKkzt~2caKkbz~2caKklx~2cfKkje~2caKkfkxx~2caKkhm~2caKkyh~2caKkzh~2caFylx~2caFqxh~2cdZzrq&OverdueCustomerReceiveMoneyInfo_startPage=1" % (number)
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
        'cookie': "JSESSIONID=E16C8068F9A76C55A9771FAC8B59C1C5; alix-server=1d267ae0c5bc3ed3ac09e32b099ebcd6",
        'postman-token': "f4baaa30-ec52-276a-8bc4-da607ea149b6"
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
            print(list_menoy[6])

def select_data():
    host = "22222.22222.2222.224"
    port = "22222"
    sid = "orcl"
    try:
        dsn = cx_Oracle.makedsn(host, port, sid)#xxxxxx
        conn = cx_Oracle.connect("xxxxx", "xxxxxxx", dsn)
        cursor = conn.cursor()
        # select appno from RP_APPLYTONO where appstate in ('6','9') and datatime between to_date('20181226 00:00:00','yyyymmdd hh24:mi:ss') and to_date('20181226 23:59:59','yyyymmdd hh24:mi:ss');
        # sql = "select appno from RP_APPLYTONO where appstate in ('6','9') and to_char(datatime,'yyyyMMdd')=to_char(sysdate,'yyyyMMdd')"
        sql = "select appno from RP_APPLYTONO where appstate in ('6','9') and datatime between to_date('20181226 00:00:00','yyyymmdd hh24:mi:ss') and to_date('20181226 23:59:59','yyyymmdd hh24:mi:ss')"
        cusr = cursor.execute(sql)
        data = list(cusr.fetchall())
        select_data = []
        if len(data) != 0:
            for date in data:
                info = date[0]
                select_data.append(info)
                return select_data
        else:
            return
        #db.commit()
        cursor.close()
    except Exception as e:
        print(e)
    finally:
        pass


def inster_data(select_data,money):
    host = "117.222.2222.2222"
    port = "1521"
    sid = "orcl"
    dsn = cx_Oracle.makedsn(host, port, sid)
    conn = cx_Oracle.connect("22222", "22222222", dsn)
    cursor = conn.cursor()
    # insert into rp_yx_settleinfo(fp_apply_no,settle_amt) values('1000289075',2332.56);
    #str = "insert into rp_yx_settleinfo(fp_apply_no,settle_amt) values('%s','%s')"
    sql = "insert into rp_yx_settleinfo(fp_apply_no,settle_amt) values('%s','%s')" % ("select_data","money")
    cusr = cursor.execute(sql)
    db.commit()
    cursor.close()

select_data()
