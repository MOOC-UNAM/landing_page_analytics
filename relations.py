import numpy as np
from get_landingpage_elements import LenTitulo
from get_landingpage_elements import get_recentviews
from get_sheet_content import lista_columna
import matplotlib
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

matplotlib.style.use('ggplot')

coursera_base_url = "https://www.coursera.org/learn/"
coursera_slugs = lista_columna(1)
courses_enrollment = lista_columna(6)

urls = []

for slugs in coursera_slugs:
    urls.append(coursera_base_url + slugs)

print("Finalizada la construcción de urls")

t = []
x = []
y = []

for link in urls:
    t.append(LenTitulo.palabras(link))
    x.append(LenTitulo.caracteres(link))
    y.append(get_recentviews(link))
    print("añadiendo datos a listas")
    print(len(x))
    print(len(y))

npx = np.array(x)
npy = np.array(y)

print(np.corrcoef(npx, npy))

df = pd.DataFrame({
    "Cantidad de caracteres": x,
    "Número de vistas": y
})

dfs = pd.DataFrame({
    "Cantidad de palabras": t,
    "Número de vistas": y
})

df_enroll = pd.DataFrame({
    "Cantidad de palabras": t,
    "Cantidad de inscritos": courses_enrollment
})


fig = px.scatter(df, x="Cantidad de caracteres", y="Número de vistas", log_y=True)
figpal = px.scatter(dfs, x="Cantidad de palabras", y = "Número de vistas", log_y=True)
figenroll = px.scatter(df_enroll, x="Cantidad de palabras", y="Cantidad de inscritos", log_y=True)

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children="Páginas de inicio"),

    html.Div(children='''
        Correlación entre cantidad de caracteres del título y vistas
    '''),
    dcc.Graph(figure=fig),

    html.Div(children='''
        Correlación entre cantidad de palabras del título y vistas
    '''),
    dcc.Graph(figure=figpal),

    html.Div(children='''
    Correlación entre cantidad de palabras e inscripciones
    '''),
    dcc.Graph(figure=figenroll)

])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)