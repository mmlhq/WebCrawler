from bs4 import BeautifulSoup
import requests
import jieba.analyse
import time

response = requests.get("https://www.sohu.com")
bs = BeautifulSoup(response.text,"html.parser")

result = bs.find_all("a")

for link in result:
    title = link.get("title")
    if title is not None:
        file = open("value1.txt","a+")
        file.write(title)
        file.close()

def read_from_file(directions):
    decode_set = ['utf-8', 'gb18030', 'ISO-8859-2', 'gb2312', 'gbk', 'Error']
    for k in decode_set:
        file = open(directions, "r", encoding=k)
        readfile = file.read()
        file.close()
        break
    return readfile

file_data = str(read_from_file('value1.txt'))
textrank = jieba.analyse.textrank

keywords_TR = textrank(file_data)
keyw_set1 = set(keywords_TR)

keyword = ' '.join(keyw_set1)
keytime = time.localtime()

print(keyword)

