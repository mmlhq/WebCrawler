# -*- coding:utf-8 -*-
# Author:MercuryYe
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

import urllib.request
import numpy as np
import pandas as pd
import jieba.analyse
from bs4 import BeautifulSoup
import time

import smtplib
from email.mime.text import MIMEText
from email.header import Header

import mysql.connector

cnx = mysql.connector.connect(user='root', password='lq8*&', host='127.0.0.1', database='tdx')
cur_tran = cnx.cursor(buffered=True)
cur_code = cnx.cursor(buffered=True)
cur_time = cnx.cursor(buffered=True)
cur_key = cnx.cursor(buffered=True)

from_addr = '28@qq.com'
password = 'lxcatzgdynjwbjbh'
to_addr = '28@qq.com'
smtp_server = 'smtp.qq.com'

url = "http://www.sohu.com/"
response = urllib.request.urlopen(url)
data = response.read()
data = data.decode('utf-8')
# soup = BeautifulSoup(data, 'html.parser')
soup = BeautifulSoup(data, 'html5lib')
# print(soup.a)
# result = soup.find_all('a', target='_blank')
result = soup.find_all('a')
result = list(set(result))
filter(None, result)
for link in result:
    title = str(link.get('title'))
    #    filewrite = open('vaule.txt','a+')
    filewrite = codecs.open('vaule.txt', 'a+', 'utf-8')
    filewrite.write(title)
    filewrite.close()


def read_from_file(directions):
    decode_set = ['utf-8', 'gb18030', 'ISO-8859-2', 'gb2312', 'gbk', 'Error']
    for k in decode_set:
        file = open(directions, "r", encoding=k)
        readfile = file.read()
        file.close()
        break
    return readfile


file_data = str(read_from_file('vaule.txt'))
textrank = jieba.analyse.textrank
keywords_TR = textrank(file_data)
keyw_set1 = set(keywords_TR)

keyword = ' '.join(keyw_set1)
keytime = time.localtime()
insert_sql = ("INSERT INTO keyword(keytime,web,keyword) values(%s,%s,%s)")
insert_data = (keytime, "www.sohu.com", keyword)
cur_tran.execute(insert_sql, insert_data)
cnx.commit()

update_time_sql = "UPDATE recordtime SET RecordTime = %s WHERE RecordID = %s"
update_time_value = (keytime, "KEY")
cur_time.execute(update_time_sql, update_time_value)
cnx.commit()

# for keyword in A:
#    insert_data = (time.localtime(),"www.sohu.com",keyword)
#    cur_tran.execute(insert_sql,insert_data)
#    cnx.commit()

qkey_time_sql = "SELECT RecordTime From recordtime WHERE RecordID='%s'" % ("KEY")
cur_time.execute(qkey_time_sql)
mytime = cur_time.fetchone()

mytime = '2020-03-07 17:34:01'
qkey_sql = "SELECT keyword FROM keyword WHERE keytime='%s'" % (mytime)
cur_key.execute(qkey_sql)
keyw = cur_key.fetchone()  # 元组
keyw_s = ''.join(keyw)  # 转字符串
keyw_list = keyw_s.split(' ')
keyw_set2 = set(keyw_list)

cur_tran.close
cur_code.close
cur_time.close
cnx.close()

diff_set = keyw_set1 - keyw_set2  # 新增加关键词

keymsg = "最新热词:\n"
keymsg = keymsg + ' '.join(diff_set) + '\n\n'
keymsg = keymsg + "目前热词:\n"
keymsg = keymsg + keyword

title = time.strftime("今日热词(%Y-%m-%d %H:%M:%S)", keytime)
msg = MIMEText(keymsg, 'plain', 'utf-8')
msg['From'] = Header(from_addr)
msg['To'] = Header(to_addr)
msg['Subject'] = Header(title)

server = smtplib.SMTP_SSL()
server.connect(smtp_server, 465)
server.login(from_addr, password)
server.sendmail(from_addr, to_addr, msg.as_string())
server.quit()