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
    titulo = sopa.find(
        "h1", class_="banner-title m-b-0 banner-title-without--subtitle")
    return titulo.text


class LenTitulo:
    def __init__(self, url):
        self.url = url

    def caracteres(self):
        '''
        Cantidad de caracteres
        '''
        titulo = get_titulo(self)
        return len(titulo)

    def palabras(self):
        titulo = get_titulo(self)
        texto = titulo.split()
        palabras_nopunct = [p for p in texto if p.isalpha()]
        return len(palabras_nopunct)


def get_recentviews(url):
    sopa = get_sopa(url)
    enrolled = sopa.find("div", class_="rc-ProductMetrics")
    try:
        return int(enrolled.text.replace("recent views", "").replace(",", ""))
    except AttributeError:
        return 0


def get_descripcion(url):
    sopa = get_sopa(url)
    descripcion = sopa.find("div", class_="m-t-1 description")
    return descripcion.text

# TODO: Las clase LenTitle y LeDescripcion son iguales. Hay que combinarlas en una sola.


class LenDescripcion:
    def __init__(self, url):
        self.url = url

    def caracteres(self):
        '''
        Cantidad de caracteres
        '''
        titulo = get_descripcion(self)
        return len(titulo)

    def palabras(self):
        titulo = get_descripcion(self)
        texto = titulo.split()
        palabras_nopunct = [p for p in texto if p.isalpha()]
        return len(palabras_nopunct)

# TODO Convertir en una Clase que recupere miniatura, 2x y 3x


def get_logos(url):
    base_url = "https://www.coursera.org/search?query="
    titulo = get_titulo(url)
    query = base_url + titulo
    sopa = get_sopa(query)
    logo = sopa.find("img", class_="product-photo")
    srcset = logo['srcset']
    return srcset.split()[0].split("?")[0]
