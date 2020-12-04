from get_sheet_content import lista_columna
from get_landingpage_elements import get_titulo, get_descripcion, get_logos
import pandas as pd

coursera_base_url = "https://www.coursera.org/learn/"
coursera_slugs = lista_columna(1)

urls = []

for slugs in coursera_slugs:
    urls.append(coursera_base_url + slugs)

logos = []
titulos = []
descripciones = []

for link in urls:
    logos.append(get_logos(link))
    titulos.append(get_titulo(link))
    descripciones.append(get_descripcion(link))
    print("datos añadidos")

print("Construyendo el DataFrame")
df = pd.DataFrame(
    {
        "Logo (ruta)": logos,
        "Título": titulos,
        "Descripción": descripciones
    }
)

print("Escribiendo el csv")
df.to_csv('csv_data/contenido_lp.csv', index=False, header=True)

print(df)
print(pd.read_csv('csv_data/contenido_lp.csv'))