from bs4 import BeautifulSoup
import requests

reponse = requests.get("https://www.163.com/")
bs = BeautifulSoup(reponse.text,"html5lib")

new_list = bs.find_all(attrs={"class":"news_default_yw"})

print(new_list)
