import requests
from bs4 import BeautifulSoup
from get_sheet_content import lista_columna
import itertools
import math
import json
import os

'''
Obtiene el contenido de una página a través de requests y BeautifulSoup
Regresa el contenido completo y analiza el HTML y XML con el módulo html.parser.
'''


def get_sopa(url):

    resultado = requests.get(url)
    try:
        resultado.status_code == 200
        contenido = resultado.content
    except:
        raise

    return BeautifulSoup(contenido, "html.parser")


'''
De la sección 'feedback', regresa el texto con la cantidad total de comentarios.
'''


def cantidad_feedback(url):
    sopa = get_sopa(url)
    return sopa.find("h2", class_="_1l2q8kho m-y-2 text-secondary").text


'''
Regresa cuántas páginas de feedback tiene un curso. Regresa un valor 'int'
'''


def get_range(url):
    cantidad_f = cantidad_feedback(url).replace(",", "")
    try:
        paginas = int(cantidad_f.split()[
            4]) / int(cantidad_f.split()[2])
        return math.ceil(paginas)
    except ValueError:
        print(cantidad_f)


'''
Función para añadir datos a JSON
'''


def escribe_json(data, filename="JSON_data/data.json"):
    with open(filename, 'w') as f:
        try:
            json.dump(data, f, indent=4, ensure_ascii=False)
        except UnicodeDecodeError:
            json.dump(data, f, indent=4, ensure_ascii=True)


'''
Función para separar la cantidad de 'likes' en los comentarios
'''


def likes(numero):
    try:
        return numero.split("(")[1].replace(")", "")
    except IndexError:
        return 0


'''
Script principal
'''
# TODO: Transformar el script en funciones
coursera_base_url = "https://www.coursera.org/learn/"
coursera_slugs = lista_columna(1)
coursera_titulos = lista_columna(0)

jsonfile = open("JSON_data/data.json", "w")

with jsonfile as file:
    try:
        data = json.load(file)
    except:
        data = []
        escribe_json(data)


# TODO: Escribir una condición para que el programa se ejecute solamente en los comentarios posteriores a la última recolección.
for i in range(1, 6):
    estrellas = "&star={}".format(i)
    for slug, titulos in zip(coursera_slugs, coursera_titulos):
        url_base = coursera_base_url + slug + "/reviews"
        url_rango = url_base + "?page=1" + estrellas
        try:
            rango = get_range(url_rango)
            for i in range(rango):
                url_paginas = url_base + "?page=" + str(i + 1) + estrellas
                sopa = get_sopa(url_paginas)
                feedback_text = sopa.select("div.rc-ReviewsList.m-b-3")
                for contenido_sopa in feedback_text:
                    texto_r = [texto.text for texto in contenido_sopa.select(
                        "div.reviewText")]
                    nombre_r = [
                        texto.text for texto in contenido_sopa.select("p.reviewerName")]
                    fecha_r = [texto.text for texto in contenido_sopa.select(
                        "div.dateOfReview")]
                    helpful = [texto.text for texto in contenido_sopa.select(
                        "div._xliqh9g.e2e-helpful-button-col > button > span > span:nth-child(2)")]
                    for t, n, f, h in zip(texto_r, nombre_r, fecha_r, helpful):
                        # TODO: desarrollar un modelo más eficiente para agregar cada testimonio al JSON
                        with open("JSON_data/data.json") as jsonfile:
                            data = json.load(jsonfile)

                            JSON_f = {
                                "testimonio": "{}".format(t),
                                "nombre": "{}".format(n[3:]),
                                "mooc": "{}".format(titulos),
                                "util": "{}".format(likes(h)),
                                "estrellas": "{}".format(estrellas[-1]),
                                "fecha": "{}".format(f),
                                "url": "{}{}".format(coursera_base_url, slug)
                            }

                            data.append(JSON_f)
                            # print("agregando datos del testimonio de {} del {}".format(n[3:], f)) # En Windws salta un EncodingErrir
                        escribe_json(data)
                        print("escribiendo en JSON")
        except AttributeError:
            pass
