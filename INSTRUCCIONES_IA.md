# Instrucciones para la IA · Práctica 1 PLN (Equipo 1)

Eres el asistente de un integrante del equipo para la Práctica 1 de Procesamiento del Lenguaje Natural. Este archivo te da el contexto de lo que ya está hecho y las reglas para hacer la parte que le toca.

**Antes de empezar:**

1. Pregúntame si soy la **Persona B** (POS y NER) o la **Persona C** (Topic Modeling) y trabaja solo en las secciones de ese rol.
2. Pídeme lo que no te haya adjuntado:
   - El enunciado `Practica1.pdf`.
   - El **material de clase de la semana 4** (carpeta `Semana4/`): las diapositivas `4-01-POS_Tagging.pdf`, `4-02-Entidades Nombradas.pdf` y `4-03-Modelado_Temas.pdf`, y el taller `Taller4.ipynb` (o `Taller4_soluciones.md`). Ahí está cómo el profesor hace POS, NER, LSA y LDA; nuestro trabajo debe seguir esa misma forma.

## Contexto

Estoy haciendo la **Práctica 1 del curso de Procesamiento del Lenguaje Natural** (Universidad Nacional de Colombia, Medellín). El enunciado completo está en `Practica1.pdf`: **es la ley; todo lo que hagamos debe cumplir exactamente lo que pide**, y no hay que agregar cosas que no pide.

**Objetivo:** clasificar noticias de **política española** como verdaderas o falsas, y analizarlas con POS Tagging, NER y Topic Modeling. Somos 3 personas (A, B y C). La entrega es el **miércoles 7 de octubre a las 12 m**.

**Lo que ya está hecho (no se debe rehacer ni modificar):**

- **Corpus (sección 1):** 5150 noticias, 2575 verdaderas y 2575 falsas.
  - Fuente 2 (corpus curado): 5000 noticias de *Spanish Political Fake News* (Universidad de Vigo, Kaggle, CC BY 4.0). Política española entre 2017 y 2023. Sus noticias falsas son **fabricadas** (alteradas o generadas con IA).
  - Fuente 1 (web scraping con BeautifulSoup): 150 noticias de España desde 2024. Las falsas son **bulos reales** verificados por Maldita y Newtral (solo la afirmación falsa). Las verdaderas son de elDiario.es (título + entradilla).
- **Preprocesamiento (sección 2):** minúsculas, sin tildes (se conserva la ñ), sin números, enlaces, saltos de línea, HTML, puntuación ni emojis.

**Estructura de la carpeta del proyecto:**

```
Practica1/
├── Practica1.pdf
├── 01_corpus.ipynb            ← NO correr (vuelve a scrapear)
├── 02_preprocesamiento.ipynb
├── corpus/Verdad/*.txt        ← corpus oficial (NO modificar)
├── corpus/Falso/*.txt
├── datos/corpus.csv           ← texto original (NO modificar)
├── datos/corpus_limpio.csv    ← texto preprocesado (NO modificar)
└── resultados/                ← aquí van nuestras tablas y gráficos
```

**`datos/corpus.csv`** (UTF-8, separador `,`): columnas

- `doc_id`: identificador único. Coincide con el nombre del `.txt` (`curado_0001`, `maldita_0003`, `eldiario_0012`…).
- `fuente`: `curado`, `maldita`, `newtral` o `eldiario`.
- `origen`: `Fuente 2: curado` o `Fuente 1: scraping`.
- `clase`: `Verdad` o `Falso`.
- `label`: 1 = verdadera, 0 = falsa.
- `url`: enlace de la noticia (vacío en las de Vigo).
- `n_palabras`: palabras del texto original.
- `texto_crudo`: el texto original, con mayúsculas, tildes y puntuación.

**`datos/corpus_limpio.csv`**: columnas `doc_id`, `fuente`, `clase`, `label`, `n_palabras_limpio` y `texto_limpio` (minúsculas, sin tildes ni puntuación). Se une con `corpus.csv` por `doc_id`.

Para leer los CSV, usar `pd.read_csv(ruta, keep_default_na=False)`, para que los campos vacíos queden como texto vacío y no como `NaN`.

**Datos útiles para el análisis:** las noticias tienen en promedio unas 54 palabras. Los bulos del scraping son más cortos (≈ 20 palabras) que las verdaderas del scraping (≈ 55).

## Reglas de trabajo

1. Trabajar en **Jupyter Notebook**, uno por sección, numerado como la sección del PDF (`03_pos.ipynb`, `04_ner.ipynb`, `07_temas.ipynb`, `08_temas_vs_clase.ipynb`…).
2. **Documentación breve**, igual que en los notebooks 01, 02, 05 y 10: un título por paso (numerado según el PDF) y, si hace falta, una o dos frases de qué se hace. Nada de explicaciones largas, justificaciones extensas ni checklists: el análisis y las justificaciones van en el informe, no en el notebook. Al final, unas conclusiones cortas en viñetas.
3. Rutas **relativas** a la carpeta del notebook: `BASE = Path.cwd()`, `DATOS = BASE / "datos"`, `RESULTADOS = BASE / "resultados"` (crearla con `mkdir(exist_ok=True)`).
4. `random_state = 42` / `SEMILLA = 42` en todo lo que tenga azar.
5. Guardar las tablas (`.csv`) y los gráficos (`.png`, `dpi=150`) en `resultados/`, con el número del notebook como prefijo.
6. **No modificar** `corpus/`, `datos/corpus.csv` ni `datos/corpus_limpio.csv`. **No correr** `01_corpus.ipynb`.
7. Si un cálculo tarda (por ejemplo, spaCy sobre 5150 textos), **guardar el resultado en `resultados/`** y cargarlo si ya existe, para no repetirlo cada vez que se reinicia el kernel.
8. Código claro y en español (nombres de variables y comentarios), apto para explicarlo en la sustentación.
9. Ante una duda sobre qué pide la práctica, **consultar el PDF** y preguntarme antes de suponer.
10. **Hacerlo como en clase:** usar las mismas librerías, funciones y parámetros del Taller 4 y de las diapositivas de la semana 4. Si hay que apartarse de eso, decirlo en una frase en el notebook y justificarlo en el informe. Así todo se puede defender en la sustentación con "lo hicimos como se vio en clase".

## Si soy la Persona B · POS y NER (secciones 3, 4 y 9 del PDF)

- **Usar `texto_crudo`** de `corpus.csv`, no el texto limpio: spaCy necesita las mayúsculas y la puntuación.
- **Modelo:** en clase (Taller 4) se usó `spacy.load("es_core_news_sm")`; ese es el punto de partida (`python -m spacy download es_core_news_sm`). Los modelos más grandes (`es_core_news_md`, `es_core_news_lg`) reconocen mejor las entidades; si se usa uno de ellos, decirlo y justificarlo en el notebook.
- **Procesar Verdad y Falso por separado** (lo pide el PDF), con `nlp.pipe(..., batch_size=...)` por eficiencia, y guardar los tokens y entidades extraídos en `resultados/`.
- **POS (sección 3):** NOUN, VERB, ADJ, ADV y PRON con frecuencia absoluta y relativa por clase. Decidir y **dejar explícito en el notebook** sobre qué total se calcula el % (recomendado: sobre todos los tokens de la clase, sin contar puntuación ni espacios). spaCy separa `PROPN` de `NOUN` y `AUX` de `VERB`; se reportan tal cual y se menciona. Pide además: el gráfico de barras comparativo, el top 10 de sustantivos, verbos y adjetivos por clase (usar el lema o la forma en minúsculas, y decirlo) y la respuesta a la pregunta del PDF.
- **NER (sección 4):** los modelos de spaCy en español etiquetan `PER`, `LOC`, `ORG` y `MISC`. Pide: la tabla Documento / Entidad / Tipo / Clase, el total por clase, la distribución porcentual, el top 10 por tipo y clase, el top 20 global por clase, los 3 gráficos, el análisis de diferencias y **al menos 5 errores reales** del modelo (entidad mal detectada, tipo equivocado o entidad no reconocida), con el texto del documento como evidencia.
- **Extra opcional:** comparar las falsas fabricadas (`fuente == "curado"` y `clase == "Falso"`) con los bulos reales (`fuente` en `maldita`/`newtral`).

## Si soy la Persona C · Temas (secciones 7, 8, 9 y 11 del PDF)

- **Usar `texto_limpio`** de `corpus_limpio.csv`.
- **Stopwords:** usar la lista de **NLTK en español** (`nltk.download("stopwords")`), **quitándole las tildes** con la misma regla del preprocesamiento (`str.maketrans("áàäâéèëêíìïîóòöôúùüû", "aaaaeeeeiiiioooouuuu")`), porque `texto_limpio` no tiene tildes. Es la misma lista que usará la Persona A en la clasificación.
- **Gensim:** `pip install gensim`. Si no instala en la versión de Python que tengan, usar un entorno con Python 3.12 o Google Colab.
- **LSA (7.1):** como en el Taller 4: TF-IDF + reducción con SVD. En clase se hizo de dos formas: con scikit-learn (`TfidfVectorizer` + `TruncatedSVD(n_components=k, random_state=42)`) y con Gensim (`corpora.Dictionary` → `doc2bow` → `TfidfModel` → `LsiModel(num_topics=k, random_seed=42)`). Para poder calcular la coherencia de LSA, conviene la versión de Gensim. Pide: las 10 palabras con más peso por tema y la interpretación manual de cada tema.
- **LDA (7.2):** con Gensim, como en el Taller 4: `LdaModel(corpus_bow, id2word=dic, num_topics=k, random_state=42, passes=10)`, recibiendo la bolsa de palabras (`corpora.Dictionary` + `doc2bow`). Las 10 palabras más representativas por tema.
- **Número de temas (7.3):** probar k = 2…10 para LSA y para LDA, calcular la **coherencia** igual que en clase (`CoherenceModel(model=..., texts=docs_tok, dictionary=dic, coherence="c_v", processes=1)`; `processes=1` evita que se cuelgue en Windows), hacer la gráfica de k vs coherencia y **justificar** el k elegido. No elegirlo arbitrariamente (el PDF lo marca en rojo).
- **Temas vs clase (sección 8):** tema dominante de cada documento con el modelo elegido. Tabla Tema / Palabras representativas / % Verdaderas / % Falsas / Interpretación, gráfico comparativo y la respuesta a la pregunta del PDF.
- **Sección 9 (con B) y 11:** al menos 3 patrones que crucen POS, NER y temas, si alguno serviría para mejorar un detector de noticias falsas, y conclusiones integrales que incluyan los resultados de la clasificación de la Persona A.

## Resultados de la Persona A (para las secciones 9 y 11)

Las secciones 5, 6 y 10 ya están hechas (`05_caracteristicas.ipynb`, `10_clasificacion.ipynb`). El archivo **`INFORME_PERSONA_A.md`** tiene sus resultados y un apartado final de **aportes para las secciones 9 y 11**: pídemelo si no lo he adjuntado. Lo esencial:

- Mejor modelo: Regresión Logística + TF-IDF + stopwords, sin stemming (F1 ponderado 0,8618 en validación cruzada).
- El clasificador detecta las falsas del corpus curado por **actores políticos fuera de lugar**: "equo", "bng", "eaj pnv", "coalicion canaria" y "nueva canarias" aparecen casi solo en las falsas. Es un patrón de **entidades** que el NER (Persona B) puede confirmar.
- Acierta el 80 % de las falsas fabricadas de Vigo pero solo el **39 % de los bulos reales** (Maldita y Newtral): las falsas fabricadas y los bulos reales son distintos, y conviene compararlos en POS, NER y temas usando la columna `fuente`.
