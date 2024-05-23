import requests
import pyperclip
from bs4 import BeautifulSoup
import validators

pyperclip.copy("")

while not validators.url(pyperclip.paste()):
    pyperclip.copy("")

request = requests.get(pyperclip.paste())
request.raise_for_status()
soup = BeautifulSoup(request.text, 'html.parser')

pList = []

for p in soup.find_all('p'):
    pList.append(p.text)

print(pList)