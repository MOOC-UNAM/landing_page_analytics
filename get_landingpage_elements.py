from bs4 import BeautifulSoup
import requests
from collections import Counter
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.common.exceptions import WebDriverException
import chromedriver_autoinstaller
import itertools
import time

def coursera_urls(archivo_csv="csv_data/ruta_cursos.csv", baseurl="https://www.coursera.org/learn/"):
    rutas = []

    df_rutas = pd.read_csv(archivo_csv)
    lista_slugs = df_rutas["Rutas"].tolist()
    for r in lista_slugs:
        rutas.append('{}{}'.format(baseurl, r))
    return rutas


def navegador():
    """Crea una ruta ejecutable para chromedriver"""
    try:
        return webdriver.Chrome()
    except SessionNotCreatedException:
        print("Actualizando Chromedriver")
        chromedriver_autoinstaller.install()
        return webdriver.Chrome()
    except WebDriverException:
        print("Instalando Chromedriver")
        chromedriver_autoinstaller.install()
        return webdriver.Chrome()


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
    rviews = sopa.find("div", class_="rc-ProductMetrics")
    try:
        return int(rviews.text.replace("recent views", "").replace(",", ""))
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


def get_logos(url):
    base_url = "https://www.coursera.org/search?query="
    titulo = get_titulo(url)
    query = base_url + titulo
    sopa = get_sopa(query)
    logo = sopa.find("img", class_="product-photo")
    srcset = logo['srcset']
    return srcset.split()[0].split("?")[0]


class Ratings:
    def __init__(self, url):
        self.url = url

    def general_rating(self):
        try:
            sopa = get_sopa(self)
            rating = sopa.find('div', class_='rc-ReviewsOverview__totals__rating')
            return float(rating.text)
        except AttributeError:
            return 0.0

    def por_estrella(self):
        estrellas = []
        sopa = get_sopa(self)
        five2one = sopa.find_all('div', class_='num-ratings')
        stars = [5, 4, 3, 2, 1]
        for s, per in zip(stars, five2one):
            percentage = per.text.replace("%", "")
            estrellas.append({
                "Estrellas": s,
                "Porcentaje": percentage
            })

        return estrellas


def get_content_rating(url):
    '''
    Regresa el porcentaje de aprobación del contenido del curso dado por los estudiantes
    '''
    try:
        sopa = get_sopa(url)
        rating = sopa.find('span', class_='expertise-rating__average-rating')
        return rating.text.replace('%', '')
    except AttributeError:
        return 0


def get_enrollment(url):
    '''
    El enrollment es un valor dinámico recuperado por JavaScript. Tenemos que recuperarlo mediante Selenium
    '''
    browser = navegador()
    browser.get(url)
    time.sleep(5)
    try:
        sopa = BeautifulSoup(browser.page_source, 'html.parser')
        enrollment = sopa.find('div', class_='_3vb6hs')
        browser.quit()
        return int(enrollment.text.replace(".", "").replace(" ya inscrito", ""))
    except AttributeError:
        return 0