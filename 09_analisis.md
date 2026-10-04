# 09 · Análisis lingüístico asentado (secciones 3 y 4)

**Práctica 1 PLN – Noticias falsas (Equipo 1, tema: política)**

Texto listo para el informe. Deja asentadas las secciones **3 (POS Tagging)** y **4 (NER)**, y el extra que compara las falsas fabricadas de Vigo con los bulos reales de Maldita y Newtral. Al final hay un aporte para la **sección 9** (análisis integrado). El cruce con temas queda pendiente de la Persona C: LSA y LDA todavía no están.

Los números salen de `03_pos.ipynb` y `04_ner.ipynb`. Las figuras y tablas están en `resultados/` (POS) y `resultados/ner/` (NER).

---

## 3. Análisis lingüístico mediante POS Tagging

Se etiquetó el texto original (`texto_crudo`), no el limpio. spaCy decide la categoría con la mayúscula, la tilde y los límites de la oración; el preprocesamiento del numeral 2 borra esas pistas. El modelo es `es_core_news_sm`, el usado en clase. Verdad y Falso se procesaron por separado.

El porcentaje de cada categoría se calculó sobre todos los tokens de esa clase, **sin puntuación ni espacios**: 139.742 tokens en verdaderas y 141.800 en falsas. spaCy no mete los nombres propios en `NOUN` ni los auxiliares en `VERB`. Esas dos etiquetas se reportan aparte y no se suman a la tabla del enunciado.

| POS | Verdaderas (cantidad) | Verdaderas (%) | Falsas (cantidad) | Falsas (%) |
|---|---:|---:|---:|---:|
| NOUN | 27.684 | 19,81 | 27.137 | 19,14 |
| VERB | 14.039 | 10,05 | 13.799 | 9,73 |
| ADJ | 8.528 | 6,10 | 8.502 | 6,00 |
| ADV | 3.199 | 2,29 | 3.152 | 2,22 |
| PRON | 4.675 | 3,35 | 4.383 | 3,09 |

*Figura: `resultados/03_pos_barras.png`. Tabla: `resultados/03_pos_tabla.csv`.*

| POS | Qué es | Verdaderas (%) | Falsas (%) |
|---|---|---:|---:|
| PROPN | Nombre propio | 13,01 | 15,25 |
| AUX | Verbo auxiliar | 2,56 | 2,47 |

*Tabla: `resultados/03_pos_propn_aux.csv`.*

**¿Hay diferencias relevantes en el uso de estas categorías?** No en las cinco que pide el enunciado. La mayor distancia es la de los sustantivos: 19,81 % frente a 19,14 % (0,67 puntos). Verbos, adjetivos, adverbios y pronombres quedan a menos de medio punto. Las dos clases escriben como un titular de política.

Donde sí hay distancia es en los nombres propios, que el modelo cuenta como `PROPN`: 15,25 % en falsas y 13,01 % en verdaderas (2,24 puntos). Los lemas más frecuentes, agrupados en minúsculas, son los mismos en las dos clases: partido, presidente, ley, tener, pedir, nuevo. En las falsas aparecen además «vers» (373) y «ver» (186) entre los sustantivos. Son el mismo fragmento de «Iniciativa vers per Catalunya», un nombre alterado de las noticias fabricadas, que el lematizador parte de dos formas. Es un problema de contenido y de etiquetado, no un estilo gramatical distinto.

*Rankings: `resultados/03_pos_top10.csv`.*

---

## 4. Reconocimiento de entidades nombradas (NER)

### 4.1 Cómo se extrajeron

Se usó el mismo texto y el mismo modelo que en el POS: `texto_crudo` y `es_core_news_sm`. El modelo pequeño se queda corto con las entidades; por eso la sección 4.5 documenta errores reales. Verdad y Falso se procesaron por separado. De cada noticia se guardó solo lo que el modelo marcó como entidad, con cuatro campos: documento, texto de la entidad, tipo y clase.

El modelo en español usa cuatro tipos: `PER` (persona), `LOC` (lugar), `ORG` (organización) y `MISC` (otros). La tabla completa está en `resultados/ner/entidades.csv` (28.604 filas). Para los rankings, «España» y «españa» cuentan como la misma entidad.

### 4.2 Total y distribución por tipo

Hay **13.949 entidades en noticias verdaderas y 14.655 en falsas**. El porcentaje de cada tipo se calcula sobre las entidades de esa clase, no sobre las palabras.

| Tipo | Significado | Verdaderas (cantidad) | Verdaderas (%) | Falsas (cantidad) | Falsas (%) |
|---|---|---:|---:|---:|---:|
| PER | Persona | 3.519 | 25,23 | 4.348 | 29,67 |
| LOC | Lugar | 4.106 | 29,44 | 4.066 | 27,74 |
| ORG | Organización | 3.285 | 23,55 | 3.128 | 21,34 |
| MISC | Otros | 3.039 | 21,79 | 3.113 | 21,24 |

*Figura: `resultados/ner/tipos.png`. Tabla: `resultados/ner/distribucion.csv`.*

### 4.3 Entidades más frecuentes

Las 10 de cada tipo y clase están en `resultados/ner/top10_tipo.csv`. Las 20 de cada clase, sin separar por tipo, están en `resultados/ner/top20.csv`. Los gráficos muestran las 15 primeras para que se lean; la tabla guarda las 20.

*Figuras: `resultados/ner/top_verdad.png` y `resultados/ner/top_falso.png`.*

| Puesto | Verdaderas | Frec. | Falsas | Frec. |
|---:|---|---:|---|---:|
| 1 | pp | 625 | gobierno | 453 |
| 2 | gobierno | 401 | iniciativa vers per catalunya | 449 |
| 3 | psoe | 339 | bng | 268 |
| 4 | vox | 233 | cristina narbona | 246 |
| 5 | congreso | 198 | eaj-pnv | 216 |
| 6 | madrid | 163 | pp | 212 |
| 7 | españa | 160 | coalición canaria | 210 |
| 8 | ciudadanos | 132 | equo | 208 |
| 9 | sánchez | 124 | congreso | 206 |
| 10 | podemos | 118 | nueva canarias | 190 |
| 11 | andalucía | 104 | madrid | 160 |
| 12 | erc | 101 | españa | 130 |
| 13 | catalunya | 90 | psoe | 110 |
| 14 | iglesias | 86 | mónica garcía | 98 |
| 15 | villarejo | 83 | cs | 93 |
| 16 | ejecutivo | 82 | rita maestre | 90 |
| 17 | pedro sánchez | 82 | andalucía | 86 |
| 18 | unidas podemos | 76 | boluarte | 85 |
| 19 | supremo | 75 | catalunya | 82 |
| 20 | feijóo | 72 | ejecutivo | 77 |

### 4.4 ¿Hay diferencias entre falsas y verdaderas?

**En los tipos, la diferencia es pequeña. En los nombres concretos, no.**

Las personas son el tipo que más se separa: 29,67 % en falsas y 25,23 % en verdaderas (4,44 puntos). Lugares, organizaciones y otros quedan a menos de 2,5 puntos. Esa comparación hay que leerla con reserva, porque el modelo confunde tipos: «Gobierno» queda casi siempre como lugar, y en las falsas mete como lugar a partidos como Coalición Canaria (210 menciones, 208 etiquetadas `LOC`) y Nueva Canarias (190, casi todas `LOC`). El porcentaje de lugares está inflado por organizaciones.

Los nombres sí cambian de clase:

| Entidad | Verdaderas | Falsas |
|---|---:|---:|
| PP | 625 | 212 |
| PSOE | 339 | 110 |
| Vox | 233 | 43 |
| Podemos | 118 | 2 |
| Iniciativa vers per Catalunya | 0 | 449 |
| BNG | 10 | 268 |
| Cristina Narbona | 2 | 246 |
| EAJ-PNV | 1 | 216 |
| Coalición Canaria | 6 | 210 |
| Equo | 5 | 208 |
| Nueva Canarias | 5 | 190 |

En las verdaderas mandan los actores centrales de la política española: PP, PSOE, Vox y Podemos. En las falsas mandan partidos regionales o minoritarios y políticos poco centrales, puestos en noticias que no les corresponden. «Iniciativa vers per Catalunya» no aparece ni una vez en las verdaderas: es un nombre alterado de las falsas fabricadas de Vigo, y el NER lo recoge 449 veces.

Esto confirma, desde otra técnica, lo que aprendió el clasificador de la Persona A. Ese modelo separa las falsas fabricadas por los mismos actores (Equo, BNG, EAJ-PNV, Coalición Canaria, Nueva Canarias, Cristina Narbona). Los conteos no coinciden número a número, porque la bolsa de palabras cuenta tokens y el NER cuenta menciones reconocidas, pero la dirección es la misma.

### 4.5 Errores del modelo

`es_core_news_sm` se equivoca con frecuencia. Cinco casos, con el documento y la frase. Cubren los tres fallos que pide el enunciado: tipo mal asignado, entidad que no lo es y entidad que debía detectarse y no se detectó.

1. **Tipo incorrecto.** En `curado_2501`, «Puigdemont» queda como `LOC`. Es una persona. Frase: «El 51% de los alemanes está en contra de la extradición de Puigdemont a España».
2. **Tipo incorrecto, y distinto dentro de la misma noticia.** En `curado_2501`, la primera «España» queda como `PER` y la segunda como `LOC`. Es un lugar. Frase: «…de Puigdemont a España. […] sea entregado a España, donde se le acusa de rebelión…».
3. **Tipo incorrecto.** En `curado_2530`, «Podemos» sale primero como `LOC` y después como `PER`. Es un partido (`ORG`). Frase: «El exatleta Roberto Sotomayor será el candidato de Podemos al Ayuntamiento de Madrid en 2023. […] La portavoz de Podemos en la Asamblea, Carolina Alonso…».
4. **Entidad que no lo es.** En `curado_2561`, «Discrepancias» se marca como `PER`. En la misma frase, «Andalucía» también queda como `PER`, aunque es un lugar, y «Sánchez», que sí es una persona, no se reconoce. Frase: «Discrepancias sobre un fondo para la financiación de Andalucía y sintonía sobre energía verde entre Moreno y Sánchez».
5. **Entidades no reconocidas.** En `curado_4698`, «Feijóo» y «Ayuso» no salen entre las entidades. «Casado» sí sale, pero como `MISC` y no como `PER`. Frase: «Feijóo asumirá el liderazgo de un PP que no ha sido capaz de pasar página de la corrupción durante la era Casado. Ayuso reconoció que su hermano cobró 280.000 euros…».

Estos errores no anulan el hallazgo del apartado 4.4. PP, PSOE, BNG y Equo sí quedan mayoritariamente como `ORG`, y Cristina Narbona como `PER`. El fallo está en los bordes: instituciones marcadas como lugar, la misma entidad con dos tipos en una sola noticia, y personas que el modelo no ve.

---

## Extra. Falsas fabricadas y bulos reales

Dentro de las falsas hay dos grupos distintos. Las **fabricadas** son las 2.500 de Vigo (`fuente == "curado"`): noticias reales alteradas o generadas. Los **bulos reales** son los 75 de Maldita (38) y Newtral (37). No se comparan por cantidad bruta: las fabricadas tienen unas 55 palabras y los bulos unas 20, y 75 textos no alcanzan para un ranking estable. Se comparan los porcentajes. Las menciones de cada nombre se leen por cada 100 noticias.

### POS

El porcentaje sigue calculándose sin puntuación ni espacios: 140.318 tokens en las fabricadas y 1.482 en los bulos.

| POS | Fabricadas (%) | Bulos reales (%) |
|---|---:|---:|
| NOUN | 19,14 | 18,83 |
| VERB | 9,72 | 10,53 |
| ADJ | 6,00 | 5,26 |
| ADV | 2,24 | 0,88 |
| PRON | 3,09 | 3,10 |
| PROPN | 15,20 | 19,57 |

*Tabla: `resultados/03_pos_fabricadas_vs_bulos.csv`.*

Sustantivos, verbos, adjetivos y pronombres siguen parecidos. Los adverbios bajan en los bulos (0,88 %), pero son solo 13 tokens: con 75 noticias cortas ese porcentaje no se puede tomar como un estilo. Lo que sí se separa es otra vez el nombre propio: 19,57 % en los bulos y 15,20 % en las fabricadas.

### NER

Hay 14.481 entidades en las fabricadas y 174 en los bulos. Por cada 100 tokens la densidad es parecida (unas 10 y unas 12): los bulos no traen menos nombres por ser más cortos. Cambia el tipo.

| Tipo | Fabricadas (%) | Bulos reales (%) |
|---|---:|---:|
| PER | 29,55 | 39,66 |
| LOC | 27,56 | 43,10 |
| ORG | 21,49 | 9,20 |
| MISC | 21,40 | 8,05 |

*Tabla: `resultados/ner/fabricadas_vs_bulos.csv`.*

Los bulos reales son sobre todo personas y lugares. Las organizaciones caen a 9,20 %. Las fabricadas reparten los cuatro tipos de forma mucho más pareja, porque están llenas de siglas de partido.

Los nombres confirman que no son el mismo fenómeno. En las fabricadas, por cada 100 noticias, aparecen unas 18 veces «Iniciativa vers per Catalunya», 11 el BNG, 10 Cristina Narbona, 9 EAJ-PNV y 8 Equo, Coalición Canaria o Nueva Canarias. En los 75 bulos, esas entidades salen **cero veces**. Lo que sí aparece en los bulos es el actor del que habla el bulo: Pedro Sánchez, 8 veces (10,7 por cada 100 bulos, frente a 0,12 por cada 100 fabricadas), y también Donald Trump, Irán, Nicolás Maduro o Estados Unidos.

Eso explica el resultado de la clasificación. El modelo acierta el 80 % de las falsas fabricadas porque aprendió esos partidos fuera de lugar, y solo el 39 % de los bulos reales porque esos bulos mencionan a los mismos protagonistas que una noticia verdadera.

---

## Aporte a la sección 9

Lo que ya se puede afirmar, cruzando POS, NER y la clasificación de la Persona A. El tercer patrón, el de temas, lo cierra la Persona C cuando estén LSA y LDA.

1. **La gramática no separa las clases; los nombres sí.** Las cinco categorías del POS difieren en menos de un punto. Los nombres propios suben un poco en las falsas, y el NER muestra que ese aumento no es «más lugares» ni «más organizaciones»: es otro reparto de actores. Un detector gana más mirando qué entidades aparecen que mirando el porcentaje de sustantivos o verbos.
2. **Las falsas fabricadas se delatan por actores fuera de lugar; los bulos reales, no.** Equo, BNG, EAJ-PNV, Coalición Canaria, Nueva Canarias y Cristina Narbona salen casi solo en las falsas de Vigo, tanto en la bolsa de palabras del clasificador como en el NER, y no aparecen en los 75 bulos de Maldita y Newtral. Esos bulos hablan de Pedro Sánchez, Trump o Maduro. El patrón serviría para detectar noticias alteradas como las de Vigo. No sirve, por sí solo, para la desinformación real, y por eso el clasificador solo acierta el 39 % de esos bulos.
3. **Pendiente de temas.** Falta ver si LSA y LDA agrupan las noticias por esos mismos actores. Si los temas de las falsas son «partido regional fuera de contexto» y los de las verdaderas son «PP, PSOE, Gobierno», el patrón queda confirmado por una tercera técnica.
