import pandas as pd
from bs4 import BeautifulSoup
import requests
import time,sys

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
articulo = input('Ingrese lo que desea buscar: ').replace(' ','-')
url= 'https://listado.mercadolibre.com.ar/'+ articulo +'_PrCategId_AD_DisplayType_LF'
#Requets.get genera un objeto del cual podemos obtener toda la informacion
r = requests.get(url).text

soup=BeautifulSoup(r,'html.parser') #html.parser es un Analizador simple de HTML

listaproductos = soup.find_all('div',{"class":"ui-search-result__content-wrapper"}) #"li" es una etiqueta de tipo "item list"
#print(listaproductos) #DEBUGGING

links_productos = []
for producto in listaproductos:
    link = producto.find("a",{"class":"ui-search-link"}).get('href') #El primer atributo "a" crea un enlace a archivos o una URL. Utilizo ".get()" para obtener el atributo "href" que es una referencia a una URL.
    links_productos.append(link)
#print(links_productos)
b=' Cargando'
with open(r'C:\Users\W4MP1\Desktop\info.txt', 'w') as file:
    file.write('Título' + '\t' + 'Precio' +'\t'+ 'Link\n')
    for link in links_productos:
        r = requests.get(link, headers=headers).text
        hun = BeautifulSoup(r, 'html.parser')
        try:
            Titulo = hun.find('h1', {'class':'ui-pdp-title'}).text.replace('\n','')
        except:
            Titulo = None
        #print(Titulo)
        try:
            Precio = hun.find('span',{'class':'price-tag-fraction'}).text
        except:
            Precio = None
        #print(Precio)
        try:
            Signo = hun.find('span',{'class':'price-tag-symbol'}).text
        except:
            Signo = None
        #print(Signo)
        file.write(Titulo +'\t'+ Signo + Precio +'\t'+ link + '\n')
        for i in range(1,4):
            sys.stdout.write(b + "." * i +'\r')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\033[2K\033[1G')
print('\nTerminé.')
        