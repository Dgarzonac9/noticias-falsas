# Práctica 1 PLN · Resumen para el equipo

**Equipo 1 · Tema: noticias falsas de política (en español)**
**Entrega:** miércoles 7 de octubre antes de las 12 m (`Practica1-E1.zip` en Classroom) · **Sustentación:** ese mismo día, de 4 a 8 pm (15 min + 5 de preguntas)

> **Para trabajar con IA:** pásenle el archivo **`INSTRUCCIONES_IA.md`** completo y el PDF `Practica1.pdf`. Este archivo (`RESUMEN_EQUIPO.md`) es solo para que **ustedes** lo lean; no hace falta dárselo a la IA.

## Estado de la práctica

| Sección del PDF | Qué es | Responsable | Estado |
|---|---|---|---|
| 1. Creación del corpus | Scraping + corpus curado + estadísticas | A | ✅ Terminado (`01_corpus.ipynb`) |
| 2. Preprocesamiento | Limpieza y normalización | A | ✅ Terminado (`02_preprocesamiento.ipynb`) |
| 3. POS Tagging | Categorías gramaticales Verdad vs Falso | **B** | ⏳ Pendiente |
| 4. NER | Entidades nombradas Verdad vs Falso + 5 errores | **B** | ⏳ Pendiente |
| 5. Extracción de características | BoW uni+bigramas, stopwords, frecuencia < 3, stemming | A | ✅ Terminado (`05_caracteristicas.ipynb` + `caracteristicas.py`) |
| 6. Ponderación | TO y TF-IDF | A | ✅ Terminado (`05_caracteristicas.ipynb`) |
| 7. Topic Modeling | LSA y LDA, coherencia k = 2…10 | **C** | ⏳ Pendiente |
| 8. Temas vs veracidad | Tema dominante, tabla y gráfico | **C** | ⏳ Pendiente |
| 9. Análisis integrado | 3 patrones POS + NER + temas | **B + C** | ⏳ Pendiente |
| 10. Clasificación | 4 algoritmos × 8 configuraciones, CV 10 | A | ✅ Terminado (`10_clasificacion.ipynb`) |
| 11. Conclusiones integrales | Cruce de todo | **C** (con todos) | ⏳ Pendiente |
| Informe + exposición | Documento final y diapositivas | Todos | ⏳ Pendiente |

## Resumen de lo que se hizo y por qué

| Tema | Decisión | Por qué |
|---|---|---|
| Tema de las noticias | **Política española** | Es el único tema con un corpus en español que cumple el mínimo de 5000 noticias balanceadas que exige el PDF. |
| Corpus curado (Fuente 2) | *Spanish Political Fake News* (Univ. de Vigo, Kaggle, CC BY 4.0). Muestra aleatoria de **2500 verdaderas + 2500 falsas** | Unas 57 000 noticias de política española (abril 2017 – junio 2023). Se evaluaron otros corpus (colombianos, multitema, COVID) y ninguno llegaba a 5000. |
| Limitación de Vigo | Sus falsas son **fabricadas**: noticias reales alteradas o generadas con IA | Hay que mencionarlo en el informe. Es probable que los modelos saquen un F1 muy alto por eso. |
| Scraping (Fuente 1) | **150 noticias** (50 por integrante) de **España, 2024 en adelante**, con **BeautifulSoup** | Mismo país y tema que Vigo, para que el modelo no aprenda "país" en vez de "veracidad". Desde 2024 para no repetir noticias de Vigo. |
| Falsas del scraping | **75 bulos reales** verificados por **Maldita (38)** y **Newtral (37)** | Guardamos solo la **afirmación falsa** (`claimReviewed` de los datos estructurados de la página), nunca el desmentido. |
| Verdaderas del scraping | **75 noticias** de la sección de política nacional de **elDiario.es**, como **título + entradilla** | Mismo formato que Vigo (título + descripción) y longitud parecida. elDiario no es uno de los medios de Vigo, así que no hay duplicados. |
| Cómo se recorrieron los sitios | Con los **sitemaps** (la lista oficial de artículos de cada sitio), respetando `robots.txt` y 2 s de pausa | La paginación de Maldita y Newtral funciona con JavaScript; el sitemap llega a los mismos artículos. |
| Revisión manual | Se excluyeron 10 falsas y 10 verdaderas no políticas. Se **conservaron 3 bulos sobre inmigración** | Esos bulos tienen fuerte carga política en España; hay que justificarlo en el informe. |
| Semilla | `random_state = 42` en todo | Cualquiera que corra los notebooks obtiene exactamente el mismo resultado. |
| Preprocesamiento | Minúsculas, sin tildes (**se conserva la ñ**), sin números, enlaces, saltos de línea, HTML, puntuación ni emojis | Es la sección 2 del PDF. El vocabulario bajó de 30 196 a 18 690 palabras distintas (−38 %). |
| Texto para cada análisis | **POS y NER → `texto_crudo`** · **Temas y clasificación → `texto_limpio`** | spaCy necesita mayúsculas y puntuación para etiquetar bien; la bolsa de palabras y los temas usan el texto limpio. |
| Stopwords | Lista de **NLTK en español, sin tildes** | El texto limpio no tiene tildes, así que la lista también debe ir sin tildes (`más` → `mas`). Así temas (C) y clasificación (A) usan la misma lista. |

## El corpus en números

| | Documentos | Palabras por doc (media) | Total palabras |
|---|---|---|---|
| Fuente 2: curado (Vigo) | 5000 | 54,45 | 272 237 |
| Fuente 1: scraping | 150 | 37,05 | 5 557 |
| **Total** | **5150** (2575 Verdad + 2575 Falso) | **53,94** | **277 794** |

**Dato para el análisis:** los bulos del scraping son mucho más cortos (≈ 20 palabras) que las noticias verdaderas del scraping (≈ 55). En Vigo, las dos clases tienen una longitud parecida (≈ 54).

## Archivos

| Archivo | Qué es | ¿Quién lo usa? |
|---|---|---|
| `corpus/Verdad/*.txt`, `corpus/Falso/*.txt` | **El corpus oficial** (lo que pide el PDF; va en el zip) | Entrega |
| `datos/corpus.csv` | Las 5150 noticias en una tabla, con el **texto original** (`texto_crudo`) | **B** (POS y NER) |
| `datos/corpus_limpio.csv` | Las mismas 5150 noticias con el **texto preprocesado** (`texto_limpio`) | **C** (temas), A (clasificación) |
| `datos/estadisticas_corpus.csv`, `datos/longitud_corpus.png` | Estadísticas de la sección 1 | Informe |
| `01_corpus.ipynb`, `02_preprocesamiento.ipynb` | Cómo se hizo todo, documentado paso a paso | Informe y sustentación |
| `datos/scraping_*.csv`, `datos/D57000_complete.csv` | Datos crudos del scraping y CSV original de Vigo | Nadie (respaldo) |

## ⚠️ Reglas para no romper nada

1. **No corran `01_corpus.ipynb` ni borren los `datos/scraping_*.csv`.** Si se vuelve a scrapear, el corpus cambia (los sitios publican bulos nuevos cada día).
2. **No modifiquen** `corpus/`, `corpus.csv` ni `corpus_limpio.csv`. Si necesitan algo distinto, créenlo en un archivo nuevo.
3. Mantengan la **estructura de carpetas**: los notebooks buscan `datos/` y `corpus/` junto a ellos.
4. Guarden sus tablas y gráficos en una carpeta `resultados/`, con el número del notebook como prefijo (por ejemplo `resultados/03_pos_tabla.csv`).
5. **Guarden los notebooks con Ctrl+S después de correrlos**, para que las salidas (tablas y gráficos) queden visibles en la entrega.

## Qué le toca a cada uno

### Persona B · Análisis lingüístico (secciones 3, 4 y 9)

- **`03_pos.ipynb`:** POS Tagging con spaCy sobre `texto_crudo`, procesando Verdad y Falso por separado. Tabla de NOUN, VERB, ADJ, ADV y PRON (cantidad y %), gráfico de barras comparativo, top 10 de sustantivos, verbos y adjetivos por clase, y la respuesta a: *¿hay diferencias relevantes entre falsas y verdaderas?*
- **`04_ner.ipynb`:** NER con spaCy sobre `texto_crudo`. Tabla Documento / Entidad / Tipo / Clase, total de entidades por clase, distribución porcentual por tipo, top 10 por tipo y top 20 global por clase, 3 gráficos, análisis de diferencias y **al menos 5 errores del NER** comentados.
- **Sección 9 (con C):** al menos 3 patrones que crucen POS, NER y temas, y si servirían para mejorar un detector.
- **Extra opcional, que suma originalidad:** comparar los resultados de POS y NER de las **falsas fabricadas** (Vigo, `fuente == "curado"`) con los **bulos reales** (`fuente` = `maldita` o `newtral`).

### Persona C · Temas e integración (secciones 7, 8, 9 y 11)

- **`07_temas.ipynb`:** LSA (con SVD) y LDA (con Gensim) sobre `texto_limpio`. Probar k = 2…10, gráfica de k vs coherencia, justificar el k elegido, y las 10 palabras principales de cada tema con su interpretación.
- **`08_temas_vs_clase.ipynb`:** tema dominante de cada documento. Tabla Tema / Palabras representativas / % Verdaderas / % Falsas / Interpretación, gráfico comparativo, y la respuesta a: *¿hay temas con presencia diferente entre falsas y verdaderas?*
- **Sección 9 (con B)** y **sección 11:** conclusiones integrales y armado del informe final.

### Persona A · Secciones 5, 6 y 10 (terminadas)

- `05_caracteristicas.ipynb` y `caracteristicas.py`: BoW con unigramas y bigramas, stopwords, filtro de frecuencia menor a 3, stemming, TO y TF-IDF.
- `10_clasificacion.ipynb`: Regresión Logística, Árbol de Decisión, KNN y SVM con las 8 configuraciones, validación cruzada de 10 pliegues, F1 ponderado, la tabla del PDF y las 3 gráficas.
- **`INFORME_PERSONA_A.md`**: el texto del informe de las secciones 1, 2, 5, 6 y 10, con los resultados reales, y un apartado de **aportes para las secciones 9 y 11**.

**Resultado principal:** el mejor modelo es Regresión Logística + TF-IDF + stopwords (F1 = 0,86). Pero el modelo aprendió a detectar las falsas *fabricadas* de Vigo por sus **partidos fuera de lugar** (Equo, BNG, EAJ-PNV, Coalición Canaria aparecen casi solo en las falsas) y **falla con los bulos reales** del scraping (39 % de acierto). B: revisen si el NER confirma ese patrón de entidades. C: úsenlo en las conclusiones.
