from bs4 import BeautifulSoup
import requests

response = requests.get("https://www.sohu.com")
bs = BeautifulSoup(response.text,"html.parser")

result = bs.find_all("a")

for link in result:
    title = link.get("title")
    if title is not None:
        file = open("value1.txt","a+")
        file.write(title)
        file.close()