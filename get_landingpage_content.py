from get_landingpage_elements import get_titulo, get_descripcion, get_logos, coursera_urls, get_enrollment, get_recentviews, Ratings, get_content_rating
import pandas as pd


urls = coursera_urls()
logos = []
titulos = []
descripciones = []
enrollments = []
vistas = []
rating_gral = []
rating_detallado = []
rating_contenido = []

for link in urls:
    print("Añadiendo datos de {}".format(get_titulo(link)))
    logos.append(get_logos(link))
    titulos.append(get_titulo(link))
    descripciones.append(get_descripcion(link))
    enrollments.append(get_enrollment(link))
    vistas.append(get_recentviews(link))
    rating_gral.append(Ratings.general_rating(link))
    rating_detallado.append(Ratings.por_estrella(link))
    rating_contenido.append(get_content_rating(link))
    

print("Construyendo el DataFrame")
df = pd.DataFrame(
    {
        "Logo (ruta)": logos,
        "Título": titulos,
        "Descripción": descripciones,
        "Inscripciones": enrollments,
        "Vistas": vistas,
        "Rating general": rating_gral,
        "Rating por estrellas": rating_detallado,
        "Rating del contenido": rating_contenido
    }
)

print("Escribiendo el csv")
df.to_csv('csv_data/contenido_lp.csv', index=False, header=True)

print(df)
print(pd.read_csv('csv_data/contenido_lp.csv'))
