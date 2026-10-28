# Informe · Secciones de la Persona A

**Práctica 1 PLN – Noticias falsas (Equipo 1, tema: política)**

Texto listo para el informe final, con los resultados reales. Cubre las secciones **1 (corpus)**, **2 (preprocesamiento)**, **5 y 6 (características y ponderación)** y **10 (clasificación)**. Al final hay un apartado con **aportes para las secciones 9 y 11** (análisis integrado y conclusiones), que arman B y C.

Las figuras y tablas citadas se generan al correr los notebooks: `datos/` (sección 1) y `resultados/` (secciones 5 a 10). El código de cada sección está en `01_corpus.ipynb`, `02_preprocesamiento.ipynb`, `05_caracteristicas.ipynb`, `caracteristicas.py` y `10_clasificacion.ipynb`.

---

## 1. Creación y caracterización del corpus

### 1.1 Tema y fuentes

El estudio se centra en **noticias de política española**. Se eligió este tema porque es el único para el que existe un corpus en español, ya etiquetado como verdadero/falso, que cumple el mínimo de 5000 muestras balanceadas que exige la práctica. Se evaluaron otras opciones (corpus colombianos, multitemáticos y de COVID-19), pero eran más pequeñas (el corpus colombiano de política tiene 3259 noticias), mezclaban temas o idiomas, o solo traían noticias falsas.

El corpus definitivo tiene **5150 noticias: 2575 verdaderas y 2575 falsas**, organizadas en las carpetas `corpus/Verdad/` y `corpus/Falso/`, un archivo `.txt` por noticia.

**Fuente 2 — corpus existente (5000 noticias).** *Spanish Political Fake News* (Otero Vizoso, Universidad de Vigo, 2023; Kaggle, licencia CC BY 4.0). Contiene 57 231 noticias de política española publicadas entre abril de 2017 y junio de 2023 (33 351 verdaderas y 23 880 falsas). Las verdaderas proceden de los diarios *Público*, *La Marea* y *El Común*; las falsas se construyeron **alterando noticias reales o generándolas con inteligencia artificial**. Cada noticia tiene título y descripción, que se unieron en un solo texto. Tras eliminar 467 duplicados, se tomó una **muestra aleatoria balanceada de 2500 verdaderas y 2500 falsas** (`random_state=42`).

**Fuente 1 — web scraping (150 noticias, 50 por integrante).** Se usaron `requests` y **BeautifulSoup**, la herramienta vista en clase. Todas las noticias son de **España y de 2024 en adelante**: del mismo país y tema que el corpus curado, para que el clasificador no aprenda a distinguir el país en vez de la veracidad, y posteriores a junio de 2023, para no repetir noticias de Vigo.

- **75 falsas:** bulos políticos reales verificados como falsos por **Maldita** (38) y **Newtral** (37). De cada verificación se extrajo únicamente la **afirmación falsa**, que estos sitios publican en sus datos estructurados (campo `claimReviewed` del esquema *ClaimReview*), y nunca el texto del desmentido.
- **75 verdaderas:** noticias de la sección de política nacional de **elDiario.es**. Se guardó **título + entradilla**, el mismo formato del corpus de Vigo.

**Decisiones del scraping:**

- **Recorrido por sitemaps.** La paginación de Maldita y Newtral se carga con JavaScript, que BeautifulSoup no ejecuta (limitación señalada en las diapositivas de la semana 2). Por eso las URLs se obtuvieron de los *sitemaps*, la lista oficial de artículos que publica cada sitio, también leídos con BeautifulSoup. Había disponibles 2746 bulos de Maldita, 2150 de Newtral y 6758 artículos de política de elDiario.es desde 2024; se recorrieron en orden aleatorio con semilla fija.
- **Scraping responsable.** Se verificó con `robots.txt` que los tres sitios permiten descargar esas páginas y se dejó una pausa de 2 segundos entre peticiones (la que pide Newtral).
- **Revisión manual.** El filtro automático de "noticia política" se basó en palabras clave, así que se descargaron 10 noticias de más por clase y se revisaron a mano. Se excluyeron 10 falsas y 10 verdaderas que no eran de política (sucesos, deporte, cadenas virales). Se conservaron tres bulos de temática migratoria por su fuerte carga política en el debate público español.

### 1.2 Métricas del corpus

Número de palabras por documento (texto original):

| | Documentos | Mean | Std | Min | 25 % | 50 % | 75 % | Max | Sum |
|---|---|---|---|---|---|---|---|---|---|
| Fuente 1: scraping | 150 | 37,05 | 19,74 | 8 | 19,25 | 36,5 | 54 | 76 | 5 557 |
| Fuente 2: curado | 5000 | 54,45 | 15,93 | 9 | 44 | 53 | 62 | 186 | 272 237 |
| Falso | 2575 | 54,31 | 17,00 | 8 | 44 | 53 | 63 | 177 | 139 841 |
| Verdad | 2575 | 53,57 | 15,60 | 20 | 43 | 52 | 61 | 186 | 137 953 |
| **Total** | **5150** | **53,94** | **16,32** | **8** | **44** | **53** | **62** | **186** | **277 794** |

*Figura: `datos/longitud_corpus.png` (distribución de la longitud por fuente y clase).*

Las dos clases tienen una longitud casi idéntica (≈ 54 palabras), lo que evita que la longitud delate la clase. La excepción está dentro del scraping: los **bulos son mucho más cortos (≈ 20 palabras)** que las noticias verdaderas (≈ 55), porque un bulo suele ser una sola afirmación. Como son solo 150 de 5150 documentos, su peso en el conjunto es pequeño.

---

## 2. Preprocesamiento

Sobre el texto de cada noticia se aplicaron las siete operaciones que pide la práctica: minúsculas, eliminación de tildes, números, enlaces, retornos de carro, elementos HTML, y signos de puntuación y emoticones. El resultado se guardó en un archivo aparte (`datos/corpus_limpio.csv`) y se conservó el texto original, porque el POS Tagging y el NER necesitan las mayúsculas y la puntuación.

**Orden de aplicación.** El orden no es el del enunciado, por razones técnicas: el HTML y los enlaces se eliminan primero, porque sus patrones dependen de signos como `<`, `/` y `.` (si se quitara antes la puntuación, `www.unal.edu.co` quedaría `wwwunaleduco` y ya no se reconocería); las tildes se quitan después de pasar a minúsculas, y los números antes que la puntuación, para que cifras como `1.300` desaparezcan completas.

**Decisiones:** la **ñ se conserva**, porque es una letra distinta y no una vocal con tilde. Se eliminan también la diéresis (ü) y los caracteres invisibles. Cada elemento borrado se reemplaza por un espacio, para no unir palabras (`PP-Vox` → `pp vox`).

**Documentos modificados por cada paso:**

| Paso | Documentos modificados | % del corpus |
|---|---|---|
| Elementos HTML | 0 | 0,00 % |
| Enlaces | 3 | 0,06 % |
| Retornos de carro / saltos de línea | 0 | 0,00 % |
| Minúsculas | 5150 | 100,00 % |
| Tildes | 5076 | 98,56 % |
| Números | 1718 | 33,36 % |
| Puntuación y emoticones | 5128 | 99,57 % |

El HTML, los enlaces y los saltos de línea casi no aparecen porque el corpus de Vigo ya venía como texto plano y en el scraping se extrajo el texto de los datos estructurados, no del HTML. Los pasos se aplican igualmente, como exige la práctica.

**Efecto:** las palabras totales apenas cambian (de 277 794 a 275 841), pero el **vocabulario se reduce un 38,1 %, de 30 196 a 18 690 palabras distintas**, porque formas como `Útil`, `útil` y `util` pasan a ser una sola.

---

## 5. Extracción de características

Las funciones están en `caracteristicas.py`, compartido por el notebook de características y el de clasificación, para que ambos usen exactamente la misma representación.

**Tokenización y bolsa de palabras.** Como el texto limpio solo contiene letras y espacios, se tokeniza separando por espacios. La bolsa de palabras contiene **unigramas** (cada token) y **bigramas** (cada token unido al siguiente, en el orden original del texto). Se usó una tokenización propia porque `CountVectorizer`, por defecto, descarta las palabras de una letra ("y", "a", "o"), lo que sería un filtro oculto en la configuración "sin ninguna técnica".

**Stopwords (dos procesos):**

1. **Lista de la librería:** las stopwords de **NLTK en español**, la librería usada en clase. Como el texto limpio no tiene tildes, se les quitaron también a la lista (`más` → `mas`); al hacerlo, algunas se fusionan (`mí` y `mi`) y la lista pasa de 313 a 306 palabras. Se eliminan antes de formar los bigramas, igual que hace scikit-learn con su parámetro `stop_words` (como en el Taller 3).
2. **Frecuencia:** se eliminan los términos que aparecen en **menos de 3 documentos** (`min_df=3`).

**Stemming:** cada palabra se reduce a su raíz con el **Snowball Stemmer de NLTK para español** (`elecciones` y `eleccion` → `eleccion`; `presidente` y `presidenta` → `president`). Se aplica después de las stopwords y antes de formar los bigramas.

**Tamaño del vocabulario (todo el corpus):**

| Paso (acumulado) | Unigramas | Bigramas | Total | Reducción |
|---|---|---|---|---|
| Bolsa de palabras sin ninguna técnica | 18 690 | 105 507 | 124 197 | — |
| + lista de stopwords de NLTK | 18 495 | 108 154 | 126 649 | −2,0 % |
| + frecuencia mínima (`min_df = 3`) | 7 205 | 4 001 | 11 206 | 91,0 % |
| + stemming | 4 678 | 5 364 | 10 042 | 91,9 % |

| Configuración de reducción | Total de términos | Reducción |
|---|---|---|
| Sin ninguna técnica | 124 197 | — |
| Solo stopwords | 11 206 | 91,0 % |
| Solo stemming | 100 903 | 18,8 % |
| Stopwords + stemming | 10 042 | 91,9 % |

**Lectura:** la lista de stopwords sola no reduce el vocabulario (incluso lo aumenta un 2 %), porque al quitar palabras se forman bigramas nuevos (en "la extradicion de puigdemont", al quitar "de" aparece `extradicion puigdemont`). La gran reducción la produce el **filtro de frecuencia**: la mayoría de los bigramas aparece en uno o dos documentos. El stemming reduce un 18,8 % por sí solo.

## 6. Ponderación de las características

- **Frecuencia absoluta (TO):** el peso de cada término es el número de veces que aparece en el documento (`CountVectorizer`).
- **TF-IDF:** multiplica la frecuencia del término en el documento por el IDF, que castiga los términos presentes en muchos documentos (`TfidfVectorizer`, con la fórmula de scikit-learn vista en la semana 2: IDF suavizado y normalización L2).

Por ejemplo, en una noticia sobre la extradición de Puigdemont, con TO todos los términos pesan 1 o 2; con TF-IDF, `extradicion` (presente en 7 documentos) pesa 0,256, mientras que `public` (presente en 506) pesa 0,114.

Las 8 configuraciones producen matrices muy **dispersas**: entre el 0,07 % y el 0,32 % de las celdas son distintas de cero, porque cada noticia tiene unas 50 palabras y el vocabulario decenas de miles de términos.

---

## 10. Técnicas de aprendizaje

### 10.1 Configuración

**Algoritmos**, con los mismos parámetros del Taller 3:

| Algoritmo | Implementación (scikit-learn) | Parámetros |
|---|---|---|
| Regresión Logística (RL) | `LogisticRegression` | `max_iter=1000, C=1.0, class_weight="balanced"` |
| Árbol de Decisión (AD) | `DecisionTreeClassifier` | `max_depth=10, min_samples_leaf=2, random_state=42` |
| K Vecinos más Cercanos (KNN) | `KNeighborsClassifier` | `n_neighbors=5, metric="cosine"` |
| Máquina de Vectores de Soporte (SVM) | `LinearSVC` | `C=1.0, class_weight="balanced", max_iter=10000` |

El único cambio respecto al taller es `max_iter=10000` en el SVM: con los conteos de TO, las 1000 iteraciones por defecto no alcanzaban para que el algoritmo convergiera.

**Ambientes:** 4 reducciones (sin ninguna técnica, solo stopwords, solo stemming, ambas) × 2 ponderaciones (TO, TF-IDF) = 8 configuraciones, y con 4 algoritmos, **32 modelos**. La entrada de cada modelo es la matriz de características y las etiquetas: **1 = verdadera, 0 = falsa**.

**Esquema de evaluación:**

1. El corpus se divide en **80 % de entrenamiento (4120 noticias) y 20 % de test (1030)** con `train_test_split` estratificado (`random_state=42`).
2. Cada modelo se evalúa con **validación cruzada de 10 iteraciones** (`StratifiedKFold(n_splits=10, shuffle=True, random_state=42)`) sobre el 80 %. Las métricas son Accuracy, y Precision, Recall y **F1 ponderados**; este último es la medida de referencia.
3. Luego se entrena con todo el 80 % y se evalúa en el **20 % de test**, como confirmación.

El vectorizador y el algoritmo van dentro de un **`Pipeline`**, de modo que el vocabulario, el filtro de frecuencia y el IDF se calculan solo con los datos de entrenamiento de cada iteración. Así se evita la fuga de información del conjunto de evaluación.

### 10.2 Resultados

Precision (P), Recall (R) y F1 ponderados, promedio de la validación cruzada de 10 iteraciones (en **negrita**, el mejor F1 de cada algoritmo):

| # | POND | STOPWORDS | STEMMING | RL P | RL R | RL F1 | AD P | AD R | AD F1 | KNN P | KNN R | KNN F1 | SVM P | SVM R | SVM F1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | TO | FALSE | FALSE | 0,8611 | 0,8570 | 0,8566 | 0,8462 | 0,7947 | 0,7866 | 0,6595 | 0,6461 | 0,6380 | 0,8533 | 0,8512 | **0,8510** |
| 2 | TO | TRUE | FALSE | 0,8576 | 0,8553 | 0,8551 | 0,8480 | 0,7978 | 0,7902 | 0,8190 | 0,8180 | **0,8178** | 0,8378 | 0,8369 | 0,8368 |
| 3 | TO | FALSE | TRUE | 0,8537 | 0,8502 | 0,8499 | 0,8420 | 0,7910 | 0,7829 | 0,6614 | 0,6510 | 0,6451 | 0,8441 | 0,8425 | 0,8423 |
| 4 | TO | TRUE | TRUE | 0,8501 | 0,8483 | 0,8481 | 0,8480 | 0,8027 | **0,7959** | 0,7957 | 0,7951 | 0,7951 | 0,8243 | 0,8238 | 0,8237 |
| 5 | TF-IDF | FALSE | FALSE | 0,8630 | 0,8495 | 0,8481 | 0,8457 | 0,7937 | 0,7855 | 0,7276 | 0,7238 | 0,7226 | 0,8554 | 0,8507 | 0,8502 |
| 6 | TF-IDF | TRUE | FALSE | 0,8716 | 0,8626 | **0,8618** | 0,8467 | 0,7966 | 0,7889 | 0,7647 | 0,7621 | 0,7615 | 0,8509 | 0,8493 | 0,8491 |
| 7 | TF-IDF | FALSE | TRUE | 0,8547 | 0,8432 | 0,8419 | 0,8424 | 0,7905 | 0,7822 | 0,7254 | 0,7211 | 0,7197 | 0,8519 | 0,8471 | 0,8466 |
| 8 | TF-IDF | TRUE | TRUE | 0,8663 | 0,8563 | 0,8553 | 0,8479 | 0,8015 | 0,7945 | 0,7614 | 0,7585 | 0,7578 | 0,8478 | 0,8461 | 0,8459 |

*La misma tabla, con los nombres completos de los algoritmos, está en `resultados/10_tabla_pdf_cv.csv`, y la de Accuracy en `resultados/10_tabla_accuracy_cv.csv`. La Accuracy no se repite en esta tabla porque coincide siempre con el Recall ponderado (es una igualdad matemática: el recall de cada clase, ponderado por su número de documentos, suma los aciertos totales).*

En el Árbol de Decisión, la precisión ponderada (≈ 0,85) es claramente mayor que el recall (≈ 0,79). El árbol, limitado a 10 niveles, solo reconoce como falsas las noticias que contienen alguno de los pocos términos que usa para decidir, y todo lo demás lo clasifica como verdadero. Con la configuración #4, de las 515 falsas del test clasifica 202 como verdaderas; pero cuando dice "falsa" acierta el 98 % de las veces (313 de 319).

### 10.3 Gráficas y análisis

*Figuras: `resultados/10_f1_maximo_por_algoritmo.png`, `resultados/10_f1_medio_por_ponderacion.png` y `resultados/10_f1_medio_por_reduccion.png`.*

**F1 máximo por algoritmo.** Los modelos **lineales** son los mejores: **Regresión Logística alcanza 0,8618** (configuración #6: TF-IDF con stopwords, sin stemming) y **SVM 0,8510** (configuración #1: TO sin ninguna técnica). Les siguen KNN (0,8178, configuración #2) y el Árbol de Decisión (0,7959, configuración #4). Es lo esperado en texto: cada noticia es un vector de miles de dimensiones, casi todas en cero, y en ese espacio los modelos lineales separan bien las clases (en las diapositivas de la semana 3, el SVM aparece como "excelente en espacios de alta dimensionalidad"). El árbol solo puede usar unas pocas palabras para decidir, y KNN se ve afectado porque, con tantas dimensiones, las distancias entre documentos se parecen mucho.

**F1 medio por ponderación y algoritmo:**

| Algoritmo | TO | TF-IDF |
|---|---|---|
| Regresión Logística | 0,8524 | 0,8518 |
| Árbol de Decisión | 0,7889 | 0,7878 |
| KNN | 0,7240 | 0,7404 |
| SVM | 0,8385 | 0,8480 |

La ponderación **casi no cambia el resultado** en Regresión Logística y en el Árbol (al árbol le da igual la escala de los pesos, porque solo compara cada término con un umbral). TF-IDF ayuda un poco al SVM (+0,010) y algo más a **KNN (+0,016)**, que compara documentos por distancia: TF-IDF baja el peso de los términos que aparecen en todas las noticias, que de otro modo hacen que todos los documentos se parezcan.

**F1 medio por técnica de reducción y algoritmo:**

| Algoritmo | Sin técnica | Solo stopwords | Solo stemming | Stopwords + stemming |
|---|---|---|---|---|
| Regresión Logística | 0,8524 | **0,8584** | 0,8459 | 0,8517 |
| Árbol de Decisión | 0,7861 | 0,7895 | 0,7825 | **0,7952** |
| KNN | 0,6803 | **0,7897** | 0,6824 | 0,7764 |
| SVM | **0,8506** | 0,8429 | 0,8444 | 0,8348 |

El efecto más grande está en **KNN: quitar stopwords sube su F1 de 0,680 a 0,790 (+0,11)**. Sin stopwords, los vecinos "más cercanos" se eligen por palabras como "de", "la" o "el", que comparten todas las noticias. En los demás algoritmos las diferencias son pequeñas: Regresión Logística mejora levemente con stopwords, el SVM rinde mejor sin ninguna técnica y el Árbol con ambas. **El stemming solo no mejora a ningún algoritmo** (entre −0,007 y +0,002): en este corpus los términos que distinguen las clases son sobre todo nombres propios (partidos y políticos), que el stemming no agrupa.

Para Regresión Logística y SVM, todas las configuraciones quedan entre 0,82 y 0,86: **la elección del algoritmo pesa más que el preprocesamiento**.

### 10.4 Confirmación en el test y mejor modelo

En los 32 modelos, el F1 en el 20 % de test queda en promedio solo **0,006 por debajo** del de la validación cruzada (la mayor diferencia es 0,031): los resultados son estables y no hay sobreajuste.

El mejor modelo es **Regresión Logística con la configuración #6 (TF-IDF, con stopwords, sin stemming)**: F1 ponderado de **0,8618 en validación cruzada** (desviación de 0,011 entre iteraciones) y **0,8494 en test**.

| Clase | Precision | Recall | F1 | Noticias en test |
|---|---|---|---|---|
| Falso (0) | 0,9227 | 0,7650 | 0,8365 | 515 |
| Verdad (1) | 0,7993 | 0,9359 | 0,8623 | 515 |
| **Ponderado** | **0,8610** | **0,8505** | **0,8494** | 1030 |

*Figura: `resultados/10_matriz_confusion_mejor.png`.* De 515 falsas, el modelo reconoce 394 y clasifica **121 como verdaderas**; solo 33 verdaderas se confunden con falsas. **El error típico es dejar pasar una noticia falsa:** cuando el modelo dice "falsa" casi siempre acierta (precisión 0,92), pero se le escapa casi una de cada cuatro (recall 0,77).

**Qué aprendió el modelo.** Los términos con más peso hacia "falsa" son partidos minoritarios o regionales y políticos poco frecuentes (`equo`, `bng`, `cristina narbona`, `eaj pnv`, `coalicion canaria`, `nueva canarias`). Hacia "verdadera" pesan los actores principales (`podemos`, `sanchez`, `psoe`, `erc`, `ayuso`, `casado`, `pp`, `vox`). Esto encaja con cómo se fabricaron las falsas de Vigo: alterando noticias reales, muchas veces **cambiando a los protagonistas**. En el corpus, "Equo" aparece en 419 noticias falsas y solo en 8 verdaderas; "BNG", en 274 frente a 10; "EAJ-PNV", en 247 frente a 1; "Cristina Narbona", en 237 frente a 2; "Coalición Canaria", en 200 frente a 6; y "Nueva Canarias", en 193 frente a 5. Por ejemplo: *"Coalición Canaria solicita a la Comunidad de Madrid los nombres y apellidos de todas las personas que imparten talleres LGTBI en los colegios"* (resultados completos en `resultados/10_terminos_clave_mejor.csv`).

### 10.5 Análisis adicional: acierto por fuente

Con el mejor modelo y la misma validación cruzada de 10 iteraciones sobre todo el corpus (`cross_val_predict`), cada noticia recibe la predicción de un modelo que no la vio al entrenar:

| Fuente | Tipo de noticia | Noticias | Acierto |
|---|---|---|---|
| Vigo (curado) | Verdaderas | 2500 | 94,8 % |
| Vigo (curado) | Falsas **fabricadas** | 2500 | 80,1 % |
| elDiario.es (scraping) | Verdaderas | 75 | 97,3 % |
| Maldita (scraping) | **Bulos reales** | 38 | 34,2 % |
| Newtral (scraping) | **Bulos reales** | 37 | 43,2 % |

El modelo reconoce bien las verdaderas de las dos fuentes y la mayoría de las falsas fabricadas, pero **con los bulos reales acierta solo 29 de 75 (38,7 %), menos que el azar**. Los bulos reales hablan de los actores principales (Pedro Sánchez, el PP, el Gobierno), justo los términos que el modelo asocia con noticias verdaderas, y no tienen los "cambios de protagonista" de las falsas de Vigo. **El F1 de 0,86 mide qué tan bien se distinguen las falsas fabricadas de Vigo, no la desinformación real.**

### 10.6 Conclusiones de la clasificación

1. **Los modelos lineales son los mejores:** Regresión Logística (F1 máximo 0,8618) y SVM (0,8510) superan a KNN (0,8178) y al Árbol de Decisión (0,7959).
2. **La ponderación importa poco:** TF-IDF iguala o mejora levemente a TO; la diferencia solo es apreciable en KNN.
3. **La eliminación de stopwords (lista + frecuencia mínima) es la reducción más útil:** reduce el vocabulario un 91 % sin perder rendimiento y es indispensable para KNN (+0,11). **El stemming no aporta** en este corpus.
4. **Configuración recomendada: Regresión Logística + TF-IDF + stopwords, sin stemming (#6)**, con el mejor F1 (0,8618) y un vocabulario 11 veces menor que sin reducción.
5. **Los resultados son confiables:** el F1 de test es muy parecido al de la validación cruzada.
6. **Limitación principal:** el modelo aprende las huellas de cómo se fabricaron las falsas del corpus curado y **no generaliza a bulos reales** (39 % de acierto).

---

## Aportes para el análisis integrado (sección 9) y las conclusiones integrales (sección 11)

Hallazgos de la Persona A para cruzar con los resultados de POS, NER y temas (B y C):

- **Patrón de entidades (para cruzar con el NER de B):** las falsas del corpus curado se caracterizan por **actores políticos fuera de contexto**, sobre todo partidos regionales y minoritarios (Coalición Canaria, Nueva Canarias, BNG, EAJ-PNV, Equo) en noticias que no les corresponden. El clasificador usa esas entidades como su señal principal. Si el NER muestra más organizaciones de este tipo en las falsas, el patrón queda confirmado desde dos técnicas distintas.
- **Las falsas fabricadas y los bulos reales no se parecen:** el clasificador detecta el 80 % de las primeras y solo el 39 % de los segundos. Conviene comparar en POS, NER y temas las falsas de `fuente == "curado"` con las de `maldita`/`newtral`.
- **Longitud:** los bulos reales son mucho más cortos (≈ 20 palabras frente a ≈ 54). Es una característica que podría añadirse a un detector, junto con las entidades.
- **Qué preprocesamiento funciona mejor:** eliminar stopwords sí ayuda (sobre todo a los modelos basados en distancia); el stemming no, porque lo que distingue las clases son los nombres propios. Esto conecta con el análisis de temas: si los temas se definen por actores políticos, el stemming tampoco debería cambiarlos mucho.
- **Mejor técnica de aprendizaje:** Regresión Logística + TF-IDF + stopwords (F1 0,86). Para un detector real haría falta entrenar con bulos verificados, no solo con falsas fabricadas.
