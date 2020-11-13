import json
import pandas as pd
import re
from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer
from wordcloud import WordCloud
from collections import Counter
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
# from sentiment_analysis_spanish import sentiment_analysis


def preprocesamiento(texto_crudo):

    solo_letras = re.sub("[^a-zA-Z]", " ", texto_crudo)
    palabras = solo_letras.lower().split()
    
    lematizador = PorterStemmer()

    palabra_vacuas = set(stopwords.words('spanish'))
    
    texto_limpio = []
    for p in palabras:
        if p not in palabra_vacuas:
            texto_limpio.append(p)
    
    stemmed_words = []
    for word in texto_limpio:
        word = lematizador.stem(word)
        stemmed_words.append(word)

    return " ".join(stemmed_words)



json_file = "JSON_data/data.json"
df = pd.read_json(json_file)
df.drop_duplicates()

estrellas_lista = []

for i in range(1, 6):
    by_star = df.loc[df['estrellas'] == i, ['testimonio', 'mooc', 'util', 'estrellas']]
    conteo = by_star.shape[0]
    estrellas_lista.append(conteo)
    
print(estrellas_lista)