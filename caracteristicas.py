"""Extracción y ponderación de características (secciones 5 y 6).

Lo usan 05_caracteristicas.ipynb y 10_clasificacion.ipynb.
"""
from functools import lru_cache, partial

import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

QUITAR_TILDES = str.maketrans("áàäâéèëêíìïîóòöôúùüû", "aaaaeeeeiiiioooouuuu")
FRECUENCIA_MINIMA = 3

nltk.download("stopwords", quiet=True)
STOPWORDS = frozenset(palabra.translate(QUITAR_TILDES) for palabra in stopwords.words("spanish"))

_stemmer = SnowballStemmer("spanish")


@lru_cache(maxsize=None)
def raiz(palabra):
    return _stemmer.stem(palabra)


def analizar(texto, quitar_stopwords=False, aplicar_stemming=False):
    """Unigramas + bigramas de un documento. Las stopwords se quitan antes del stemming y de formar los bigramas."""
    tokens = texto.split()
    if quitar_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS]
    if aplicar_stemming:
        tokens = [raiz(t) for t in tokens]
    bigramas = [f"{a} {b}" for a, b in zip(tokens, tokens[1:])]
    return tokens + bigramas


def construir_vectorizador(ponderacion, quitar_stopwords, aplicar_stemming):
    """Vectorizador TO o TF-IDF. El filtro de frecuencia (min_df=3) se aplica junto con las stopwords."""
    analizador = partial(analizar, quitar_stopwords=quitar_stopwords, aplicar_stemming=aplicar_stemming)
    min_df = FRECUENCIA_MINIMA if quitar_stopwords else 1
    if ponderacion == "TO":
        return CountVectorizer(analyzer=analizador, min_df=min_df)
    if ponderacion == "TF-IDF":
        return TfidfVectorizer(analyzer=analizador, min_df=min_df)
    raise ValueError(f"Ponderación desconocida: {ponderacion}")


# Las 8 configuraciones de la sección 10, en el orden del PDF
CONFIGURACIONES = [
    {"#": 1, "POND": "TO", "STOPWORDS": False, "STEMMING": False},
    {"#": 2, "POND": "TO", "STOPWORDS": True, "STEMMING": False},
    {"#": 3, "POND": "TO", "STOPWORDS": False, "STEMMING": True},
    {"#": 4, "POND": "TO", "STOPWORDS": True, "STEMMING": True},
    {"#": 5, "POND": "TF-IDF", "STOPWORDS": False, "STEMMING": False},
    {"#": 6, "POND": "TF-IDF", "STOPWORDS": True, "STEMMING": False},
    {"#": 7, "POND": "TF-IDF", "STOPWORDS": False, "STEMMING": True},
    {"#": 8, "POND": "TF-IDF", "STOPWORDS": True, "STEMMING": True},
]
