#LINK USADO: https://www.epa.gov/web-policies-and-procedures/web-standard-pdf-links

import requests
import pyperclip
import os
from bs4 import BeautifulSoup
import validators


pyperclip.copy("")

while not validators.url(pyperclip.paste()):
    pyperclip.copy("")

request = requests.get(pyperclip.paste())
request.raise_for_status()
bSoup = BeautifulSoup(request.text, 'html.parser')

aList = bSoup.find_all('a')

for a in aList:
    if ('.pdf' in a.get('href', []).lower()):
        print(f"DESCARGANDO {a.get('href')}")
        title = "".join(filter(str.isalnum, bSoup.find("title").text))
        if not os.path.exists(title):
            os.makedirs(title)
        os.chdir(title)
        
        res = requests.get(a.get('href'))
        pdf = open(a.get('href').split("/")[-1].split("?")[0], 'wb')
        pdf.write(res.content)
        pdf.close()