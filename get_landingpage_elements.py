from bs4 import BeautifulSoup
import requests
from collections import Counter
import numpy as np

def get_sopa(url):

    resultado = requests.get(url)
    try:
        resultado.status_code == 200
        contenido = resultado.content
    except:
        raise

    return BeautifulSoup(contenido, "html.parser")

def get_titulo(url):
    sopa = get_sopa(url)
    return sopa.find("h1", class_="banner-title m-b-0 banner-title-without--subtitle")


class LenTitulo:
    def __init__(self, url):
        self.url = url
    
    def caracteres(self):
        '''
        Cantidad de caracteres
        '''
        titulo = get_titulo(self)
        return len(titulo.text)
    
    def palabras(self):
        titulo = get_titulo(self)
        texto = titulo.text.split()
        palabras_nopunct = [p for p in texto if p.isalpha()]
        return len(palabras_nopunct)


def get_recentviews(url):
    sopa = get_sopa(url)
    enrolled = sopa.find("div", class_="rc-ProductMetrics")
    try:
        return int(enrolled.text.replace("recent views", "").replace(",", ""))
    except AttributeError:
        return 0


