import requests
import pyperclip
import os
from bs4 import BeautifulSoup
import validators
import time
from selenium import webdriver
from collections import Counter 

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

def scrollTroughPage(url):
    driver = webdriver.Chrome()
    driver.get(url)
        
        
    screenHeight = driver.execute_script("return window.screen.height;")
    maxScrolls = 50
    scrollCount = 0
    
    while scrollCount < maxScrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        maxHeight = driver.execute_script("return document.body.scrollHeight")
        if maxHeight == screenHeight:
            break
        screenHeight = maxHeight
        scrollCount += 1
    scrolledLink = driver.page_source
    driver.quit()
    return scrolledLink

def productInfo(url):
    
    main = requests.get(url)
    main.raise_for_status()
    main = BeautifulSoup(main.text, 'html.parser')

    title = main.find(class_ = "ui-pdp-title").text
    
    if "MLA-" in url:
        commonWords = "*No hay valoraciones*"
        rating = "*No hay valoraciones*"
    else:

        review = BeautifulSoup(scrollTroughPage("https://www.mercadolibre.com.ar/noindex/catalog/reviews/" + ((url).split("#")[0]).split("/")[-1] + "?noIndex=true&access=view_all&modal=true&controlled=true"), 'html.parser')
        
        rating = review.find(class_ = "ui-review-capability__rating__average ui-review-capability__rating__average--desktop").text

        reviewList = list(map(lambda x: x.text,review.find_all(role = "presentation")))
        reviewListWords = []
        for x in reviewList:
            for y in x.split():
                reviewListWords.append("".join(list(filter(str.isalnum ,list(y.lower())))))

        minWordLen = 5
        wordCount = 10

        commonWords = list(filter(lambda x: len(x) > minWordLen ,list(map(lambda x: x[0] ,Counter(reviewListWords).most_common()))))[0:wordCount]
        
    #title, commonWords, rating

    w, h = A4
    c = canvas.Canvas(f"{title}.pdf")
    text = c.beginText(50, h - 50)
    text.setFont("Times-Roman", 15)
    text.textLine("Nombre del producto:")
    text.textLine(title)
    text.textLine("Sitio de ventas: Mercado Libre")
    text.textLine(f"Promedio de valoraciones: {rating}")
    text.textLine("Palabras clave más frecuentes:")
    if type(commonWords) == list:
        for i in range(len(commonWords)):
            text.textLine(f"- {commonWords[i]}")
    else:
        text.textLine(commonWords)
    c.drawText(text)
    c.save()


response = input("Te gustaria (1)Buscar el producto en mercado libre o (2)Ingresar el link del producto manualmente? : ")
while response != "1" and response != "2":
    response = input("Te gustaria (1)Buscar el producto en mercado libre o (2)Ingresar el link del producto manualmente? : ")

if response == "1":
    search = input("Que te gustaria buscar en mercado libre?: ")
    search = BeautifulSoup(scrollTroughPage("https://listado.mercadolibre.com.ar/" + search), 'html.parser')
    nextPage = False
    finished = False
    while True:
        productList = list(filter(lambda x: 'item' in x, list(map(lambda x: x.get('href'),search.find_all('a')))))

        print("Las opciones de productos son:")

        for i in range(len(productList)):
            res = requests.get(productList[i])
            res.raise_for_status()
            res = BeautifulSoup(res.text, 'html.parser')
            title = res.find(class_ = "ui-pdp-title").text
            price = res.find(class_ = "andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact").text
            productList[i] = (price, title, productList[i])
            print(f"({i + 1}) {productList[i][0]} {productList[i][1]}")

        print(f"({len(productList) + 1}) *O avanza a siguiente pagina del catalogo*")

        answer = ""
        
        while (not answer.isdecimal()):
            answer = input("Que opcion te gustaria seleccionar? : ")
            if answer.isdecimal():
                if int(answer) == len(productList) + 1:
                    if search.find(string = "Siguiente") != None:
                        nextPage = True
                if not (int(answer) <= len(productList) and int(answer) > 0):
                    answer = ""
        
        for i in range(len(productList)):
            if str(i + 1) == answer:
                productLink = productList[i][2]
                finished = True
        
        if finished == True:
            break

        if nextPage:
            search = BeautifulSoup(scrollTroughPage(search.find(string = "Siguiente").get("href")), 'html.parser')
            nextPage = False
    print(productLink)
    productInfo(productLink)


else:

    print("Copie el link del producto al portapapeles")

    pyperclip.copy("")
    
    while (not validators.url(pyperclip.paste())) and (not "mercadolibre" in pyperclip.paste()):
        pyperclip.copy("")

    productInfo(pyperclip.paste())