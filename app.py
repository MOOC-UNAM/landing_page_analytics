import numpy as np
from get_landingpage_elements import LenTitulo, LenDescripcion, get_recentviews
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
z = []
v = []

for link in urls:
    t.append(LenTitulo.palabras(link))
    x.append(LenTitulo.caracteres(link))
    z.append(LenDescripcion.caracteres(link))
    v.append(LenDescripcion.palabras(link))
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

df_desc = pd.DataFrame({
    "Cantidad de caracteres (descripción)": z,
    "Número de vistas": y
})

df_descr = pd.DataFrame({
    "Cantidad de palabras (descripción)": v,
    "Número de vistas": y
})

df_enroll = pd.DataFrame({
    "Cantidad de palabras": t,
    "Cantidad de inscritos": courses_enrollment
})


fig = px.scatter(df, x="Cantidad de caracteres",
                 y="Número de vistas", log_y=True)
figpal = px.scatter(dfs, x="Cantidad de palabras",
                    y="Número de vistas", log_y=True)
figenroll = px.scatter(df_enroll, x="Cantidad de palabras",
                       y="Cantidad de inscritos", log_y=True)

figdes = px.scatter(df_desc, x="Cantidad de caracteres (descripción)",
                    y="Número de vistas", log_y=True)
figdesc = px.scatter(
    df_descr, x="Cantidad de palabras (descripción)", y="Número de vistas", log_y=True)

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children="Páginas de inicio", style={'text-align': 'center'}),

    html.Div(children='''
        Correlación entre cantidad de caracteres del título y vistas
    '''),
    dcc.Graph(figure=fig),

    html.Div(children='''
        Correlación entre cantidad de palabras del título y vistas
    '''),
    dcc.Graph(figure=figpal),

    html.Div(children='''
        Correlación entre cantidad caracteres de la descripción y vistas
    '''),
    dcc.Graph(figure=figdes),

    html.Div(children='''
        Correlación entre cantidad de palabras de la descripción y vistas
    '''),
    dcc.Graph(figure=figdesc),

    html.Div(children='''
    Correlación entre cantidad de palabras e inscripciones
    '''),
    dcc.Graph(figure=figenroll)

])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
