# Seguimiento 2026-2: analisis de algoritmos en bibliometria

## Proposito

Construir una aplicacion academica que procese los resumenes (abstracts) de un corpus controlado de 20 articulos cientificos sobre inteligencia artificial generativa. La aplicacion contara los terminos del corpus y comparara tres algoritmos de ordenamiento no basados en comparaciones para obtener un ranking de frecuencia: Counting Sort, Radix Sort y Bucket Sort.

El proyecto busca que el codigo sea facil de leer y explicar. La implementacion debe permitir relacionar algoritmos clasicos y estructuras de datos con el procesamiento computacional de texto, y servir como base para el analisis teorico y la medicion empirica solicitados en el seguimiento.

## Alcance indicado por el documento del curso

El PDF `Seguimiento 2026-2.pdf` establece estos requisitos. El archivo PDF es material de referencia del curso; sus requisitos se incorporan aqui como especificacion del proyecto.

- El corpus es estatico y controlado: 20 articulos cientificos entregados por el docente en formato PDF.
- El analisis debe enfocarse estrictamente y de forma primordial en el abstract de cada articulo.
- El titulo y los autores tambien pueden extraerse, pero solo para los requerimientos funcionales que necesiten cruzar esa informacion. No forman parte del texto principal que se cuenta, salvo acuerdo explicito posterior.
- Se debe generar el ranking de terminos mas frecuentes del corpus completo.
- El ranking debe implementarse mediante Counting Sort, Radix Sort y Bucket Sort, algoritmos que no ordenan comparando directamente cada par de elementos.
- El informe debe explicar por que cada algoritmo alcanza la complejidad asintotica pertinente (`O(n + k)` u `O(n)`), especificando que representan `n` y `k` en la implementacion concreta y bajo que supuestos aplica el analisis.
- Se deben medir los tiempos reales de ejecucion de cada implementacion en milisegundos sobre la lista de frecuencias del corpus completo.
- Se debe presentar una tabla o grafico con los 15 terminos mas frecuentes, obtenido con cada uno de los tres algoritmos.

## Decisiones acordadas

- **Lenguaje:** Python 3.11 o superior.
- **Framework:** no se usara un framework. El proyecto es una aplicacion pequena de procesamiento por lotes: lee un corpus fijo, procesa texto y ejecuta algoritmos. La biblioteca estandar de Python alcanza para esta base, evita conceptos y dependencias innecesarios y permite concentrarse en explicar los algoritmos. Se puede agregar una biblioteca puntual para extraer texto de PDF si hace falta; eso no requiere un framework.
- **Corpus:** los 20 PDF entregados se guardan en `data/raw/` y se versionan junto con el proyecto, tal como se acordo.
- **Texto:** los articulos estan en ingles. La normalizacion sera opcional: cuando este activada, convierte a minusculas y quita diacriticos, conservando la `ñ`; cuando este desactivada, respeta mayusculas y diacriticos. No se eliminaran stopwords.
- **Representacion:** las frecuencias se mantienen en un diccionario de Python (`term -> frequency`). Para ordenar se convertiran en pares `(term, frequency)`, que conservan el termino asociado a su frecuencia.
- **Informe:** se preparara mas adelante en formato IEEE; el usuario se encargara de las normas de presentacion.
- **Idioma del codigo:** nombres de variables, funciones, modulos y clases en ingles; comentarios y docstrings explicativos en espanol.
- **Estilo:** funciones pequenas, nombres descriptivos, flujo directo y estructuras de datos conocidas. Evitar abreviaturas opacas, metaprogramacion, clases innecesarias y dependencias sin justificacion.
- **Medicion:** los tres algoritmos reciben los mismos datos y se mide solamente el ordenamiento, excluyendo extraccion y conteo. No se agregaran repeticiones o estadisticas no solicitadas por el curso.
- **Commits:** el usuario hara los commits manualmente. No hacer commits ni subir cambios a GitHub.

## Estructura propuesta

```text
.
├── README.md
├── pyproject.toml
├── data/
│   ├── raw/                 # Los 20 PDF originales del corpus
│   └── processed/           # Texto y datos derivados; fuera de Git
├── reports/                 # Informe y resultados exportados
├── src/
│   └── bibliometric_analysis/
│       ├── cli.py           # Interfaz de linea de comandos
│       ├── text_processing.py
│       └── ranking/
│           ├── counting_sort.py
│           ├── radix_sort.py
│           └── bucket_sort.py
└── tests/                   # Pruebas de las funciones y algoritmos
```

La estructura inicial reserva modulos por responsabilidad; los modulos de algoritmos aun no contienen implementaciones. `data/raw/` contiene los PDF del corpus y debe mantenerse en el repositorio. Los datos derivados se excluyen de Git para evitar almacenar resultados generados que pueden reconstruirse.

## Responsabilidades por modulo

| Modulo | Responsabilidad prevista |
| --- | --- |
| `text_processing.py` | Normalizar el texto del abstract y contar terminos una vez se acuerden las reglas de limpieza. |
| `ranking/counting_sort.py` | Ordenar las frecuencias usando conteo de claves dentro de un rango conocido. |
| `ranking/radix_sort.py` | Ordenar frecuencias enteras procesando sus digitos. |
| `ranking/bucket_sort.py` | Distribuir las frecuencias en cubetas y ordenarlas segun la variante documentada. |
| `cli.py` | Conectar lectura de corpus, procesamiento, ranking y exportacion mediante comandos comprensibles. |
| `tests/` | Verificar casos normales, limites, entradas vacias y que los tres algoritmos produzcan el mismo orden esperado. |

Esta separacion es una propuesta inicial. Debe adaptarse si el formato entregado por el docente o las reglas de extraccion requieren otros modulos.

## Reglas de texto y datos pendientes de acordar

El documento no especifica como extraer el abstract de cada PDF ni como limpiar el texto. La regla acordada para normalizar es opcional y no elimina stopwords:

- Con normalizacion activada, pasar a minusculas y quitar diacriticos, preservando la letra `ñ` (por ejemplo, `é` pasa a `e`, pero `ñ` sigue siendo `ñ`).
- Con normalizacion desactivada, preservar mayusculas y diacriticos. En ambos modos se requiere una tokenizacion consistente, que separara las palabras de la puntuacion sin eliminar palabras por ser comunes.
- No aplicar stopwords, stemming ni lematizacion.
- Como identificar el abstract cuando los PDF tengan formatos distintos y como registrar extracciones fallidas para revision manual.
- La unidad de ranking es el par `(termino, frecuencia)`. El diccionario `term -> frequency` es una forma sencilla de construir y consultar el conteo; antes de ordenar, sus entradas se convierten en pares para que nunca se pierda la relacion entre palabra y cantidad.
- No se anadira un criterio adicional de desempate. Si varios terminos tienen la misma frecuencia, se acepta el orden que produzca la implementacion del algoritmo, siempre que no se pierdan terminos ni frecuencias.

No se debe asumir que texto obtenido por extraccion automatica del PDF es correcto sin una forma de inspeccion o validacion.

## Requisitos de los algoritmos y medicion

- Documentar en cada algoritmo el contrato de entrada y salida, la idea general y la complejidad con sus supuestos.
- Ordenar de forma descendente para el ranking final; si internamente conviene ordenar ascendente, hacer explicita la conversion.
- No agregar un paso de desempate. Validar que los resultados ordenen correctamente por frecuencia y conserven los terminos empatados; el orden relativo de elementos con igual frecuencia puede variar entre algoritmos.
- Comparar el resultado de los tres algoritmos y confirmar que el top 15 coincide.
- Medir en milisegundos con el mismo conjunto de entrada; ejecutar varias repeticiones puede ayudar a reducir ruido, pero la cantidad de repeticiones y la estadistica reportada quedan pendientes de acuerdo.
- Separar la medicion de ordenamiento del tiempo de lectura, extraccion y conteo.
- Explicar que `n` y `k` representan valores distintos segun el algoritmo (por ejemplo, numero de elementos y rango de claves); no presentar `O(n)` sin describir los supuestos sobre el rango, los digitos o la distribucion en cubetas.

## Convenciones de contribucion

- Usar nombres en ingles, completos y especificos: `count_word_frequencies`, no nombres vagos como `process_data`.
- Escribir comentarios y docstrings en espanol para explicar decisiones o reglas que no sean obvias; no comentar cada linea.
- Preferir funciones cortas con una responsabilidad clara y tipos de entrada y salida entendibles.
- Evitar codigo duplicado, variables globales mutables y dependencias externas que no sean necesarias.
- Mantener el ordenamiento y la medicion separados del procesamiento de documentos.
- Cuando una regla del curso no este definida, dejarla documentada como decision pendiente en lugar de ocultarla como supuesto.

## Preparacion del entorno (propuesta)

Se recomienda Python 3.11 o superior y un entorno virtual local:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

La base actual no agrega dependencias de ejecucion. Cuando acordemos el formato real de entrada y la forma de extraer PDF, se elegira una biblioteca adecuada y se fijara su version. La interfaz de linea de comandos aun esta pendiente; no hay un comando de analisis implementado todavia.

## Algoritmos en palabras sencillas

Los tres metodos deben ordenar por la frecuencia numerica, sin comparar repetidamente un elemento contra otro como haria un algoritmo de comparacion tradicional:

- **Counting Sort** cuenta cuantas veces aparece cada valor de frecuencia y reconstruye el orden recorriendo esos conteos. Es directo cuando los valores son enteros y su rango no es demasiado grande. Para pares termino-frecuencia, el conteo debe conservar o recuperar los terminos asociados a cada valor.
- **Radix Sort** ordena enteros por partes (por ejemplo, digito por digito), desde la posicion menos significativa. En cada pasada usa un ordenamiento estable para conservar el orden logrado en las pasadas anteriores. Los elementos con igual frecuencia quedan juntos, pero el orden entre ellos depende del orden estable usado y de la entrada.
- **Bucket Sort** distribuye los valores en grupos o cubetas segun su rango, ordena cada cubeta y concatena los grupos. Su rendimiento lineal depende de una distribucion apropiada y de una forma eficiente de ordenar cada cubeta; no es lineal para cualquier entrada por defecto.

En estos algoritmos, "no basado en comparaciones" significa que aprovechan que las claves son numeros enteros o pertenecen a un rango/dominio que se puede recorrer. No significa que cualquier dato o variante tenga automaticamente complejidad lineal. Como varios terminos pueden tener la misma frecuencia, el ranking debe conservarlos todos. No se requiere ordenar alfabeticamente los terminos que empaten.

## Commits personales

El usuario hara los commits. Para mantener un historial facil de revisar:

1. Revisar `git status` y `git diff` para confirmar que solo se incluyan los cambios esperados.
2. Agrupar cambios relacionados en un commit; evitar mezclar estructura, corpus y una funcionalidad no relacionada.
3. Usar un asunto corto en modo imperativo, por ejemplo `Add project structure` o `Implement counting sort`.
4. Agregar una descripcion breve cuando el cambio necesite contexto. No incluir PDF u otros archivos sensibles si el commit no debe contenerlos.
5. Revisar el commit con `git show --stat` despues de crearlo.

## Estado actual

La estructura y la especificacion inicial estan preparadas y los 20 PDF estan en `data/raw/`. La extraccion de PDF, el procesamiento del corpus, los algoritmos y la interfaz se implementaran despues de definir la extraccion de abstracts. La normalizacion opcional ya esta acordada y no se eliminaran stopwords ni se agregara un desempate. El informe se abordara despues de terminar la aplicacion.
