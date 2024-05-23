#LINK USADO: https://www.python.org/
#Hay que cambiarlo...
import requests
import pyperclip
from bs4 import BeautifulSoup
import validators

pyperclip.copy("")

while not validators.url(pyperclip.paste()):
    pyperclip.copy("")

request = requests.get(pyperclip.paste())
request.raise_for_status()
bSoup = BeautifulSoup(request.text, 'html.parser')

pagination = [pyperclip.paste()]

for a in bSoup.find_all('a'):
    
    if validators.url(a.get('href')):
        pagination.append(a.get('href'))

paragraphList = []

for link in pagination:
    res = requests.get(link)
    """res.raise_for_status()"""
    soup = BeautifulSoup(res.text, 'html.parser')

    for p in soup.find_all('p'):
        paragraphList.append(p.text)

print(paragraphList)