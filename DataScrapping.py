import pandas as pd
from bs4 import BeautifulSoup
import requests
import time,sys
import xlsxwriter
import os


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
articulo = input('Ingrese lo que desea buscar: ').replace(' ','-')
url= 'https://listado.mercadolibre.com.ar/'+ articulo +'_PrCategId_AD_DisplayType_LF'
#Requets.get genera un objeto del cual podemos obtener toda la informacion
r = requests.get(url).text

soup=BeautifulSoup(r,'html.parser') #html.parser es un Analizador simple de HTML

listaproductos = soup.find_all('div',{"class":"ui-search-result__content-wrapper"}) #"li" es una etiqueta de tipo "item list"
#print(listaproductos) #DEBUGGING


filepath = os.path.expanduser(os.getenv('USERPROFILE'))
Excel = xlsxwriter.Workbook(filepath + r'\Desktop\Datos.xlsx') #Creamos Excel
wsheet = Excel.add_worksheet()

fila = 1
titulos = []
precios = []
monedas = []
links = []
sig = True
wsheet.write(0, 0, 'Título')
wsheet.write(0, 1, 'Moneda')
wsheet.write(0, 2, 'Precio')
wsheet.write(0, 3, 'Link')
while(sig):
    titulos.clear()
    precios.clear()
    monedas.clear()
    links.clear()
    #print('Lista desde 0')
    for producto in listaproductos:
        #print(len(listaproductos))

        titulo = producto.find("h2",{"class":"ui-search-item__title"}).text.replace('\n','') #El primer atributo "a" crea un enlace a archivos o una URL. Utilizo ".get()" para obtener el atributo "href" que es una referencia a una URL.
        titulos.append(titulo)

        precio = producto.find('span',{'class':'price-tag-fraction'}).text
        precios.append(precio)

        moneda = producto.find('span',{'class':'price-tag-symbol'}).text
        monedas.append(moneda)

        link = producto.find("a",{"class":"ui-search-link"}).get('href')
        links.append(link)
    b=' Cargando'
    for titulo, precio, moneda, link in zip(titulos, precios, monedas, links):
        #print(Signo)   
        wsheet.write(fila,0,titulo)
        wsheet.write(fila,1,moneda)
        wsheet.write(fila,2,(precio))
        wsheet.write(fila,3,link)
        fila+=1
        for i in range(1,4):
            sys.stdout.write(b + "." * i +'\r')
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\033[2K\033[1G')
    print('Termine archivo')
    try:
        link_sig = soup.find('div',{'class':'ui-search-pagination'})
        link_sig = link_sig.find('li',{'class':'andes-pagination__button andes-pagination__button--next'}) #Buscamos la "li" que contenga el sig.
        link_sig = link_sig.find('a', {'class':'andes-pagination__link ui-search-link'}).get('href')  #Obtenemos la URL de la siguente pagina.
        r = requests.get(link_sig).text
        soup=BeautifulSoup(r,'html.parser')
        listaproductos = soup.find_all('div',{"class":"ui-search-result__content-wrapper"})
        print('Pág. siguiente')
    except:
        sig = False
Excel.close()
print('\nTerminé.')