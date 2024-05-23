import requests
import os
import pyperclip
from bs4 import BeautifulSoup
import validators

pyperclip.copy("")

while not validators.url(pyperclip.paste()):
    pyperclip.copy("")

request = requests.get(pyperclip.paste())
request.raise_for_status()
request = BeautifulSoup(request.text, 'html.parser').prettify()

i = 0
while os.path.exists('index' + str(i) + '.txt'):
        i += 1
    
file = open('index' + str(i) + '.txt', 'wb')
file.write(request.encode())
file.close()