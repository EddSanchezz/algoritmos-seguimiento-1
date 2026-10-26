# Análisis de algoritmos en bibliometría

El proyecto procesa los abstracts de 20 artículos científicos en PDF, cuenta sus términos y los ordena por frecuencia. Título y autores se extraen como metadatos, pero no se cuentan.

## Flujo

```text
PDF → extracción de abstracts → minúsculas y filtro de palabras comunes
    → conteo → pares (término, frecuencia) → algoritmo → tiempo y top 15
```

Cada punto de entrada ejecuta un solo algoritmo sobre el mismo corpus. El tiempo medido incluye únicamente el ordenamiento, no la lectura de PDF ni el conteo.

## Organización

```text
data/raw/                              # Los 20 artículos PDF
data/processed/                        # Reservado para resultados
src/bibliometric_analysis/
├── pdf_extractor/pdf_extractor.py     # Extrae título, autores y abstract
├── text_processing.py                 # Normaliza, filtra y cuenta términos
├── main_support.py                    # Prepara los datos y muestra rankings
├── main.py                            # Ejecuta Counting Sort
├── main_radix_sort.py                 # Ejecuta Radix Sort
├── main_bucket_sort.py                # Ejecuta Bucket Sort
└── ranking/                           # Implementaciones de los algoritmos
```

### Extracción y conteo

El extractor devuelve un registro por PDF con `id`, `file`, `title`, `authors`, `abstract` y `warnings`. Usa la primera página para localizar los metadatos y el abstract, y el resto del PDF para reconocer palabras compuestas con guion. También elimina una referencia incrustada en el abstract del artículo 14.

Cada punto de entrada vuelve a extraer los 20 PDF; por eso cada ejecución tarda alrededor de 80 segundos. Ese tiempo queda fuera de la medición del algoritmo.

Los abstracts quedan en minúsculas y conservan sus acentos. `text_processing.py` mantiene una lista fija de palabras comunes en inglés —por ejemplo, `the`, `and`, `for`, `of`, `in` y `to`— y las excluye antes de contar. No se cuentan tokens numéricos ni se aplican stemming o lematización. Los compuestos como `ai-driven` se conservan como un término.

## Counting Sort

Cada algoritmo recibe pares `(término, frecuencia)`. Counting Sort busca la frecuencia máxima, crea una cubeta para cada frecuencia posible, agrega cada par a su cubeta y recorre las cubetas de mayor a menor. Los términos empatados conservan el orden de entrada.

Si `n` es la cantidad de términos distintos y `k` es la cantidad de frecuencias posibles (`frecuencia_máxima + 1`), el tiempo y el espacio adicional son `O(n + k)`.

## Ejecución individual

Instalar desde la raíz del proyecto:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Ejecutar un algoritmo a la vez:

```powershell
python -m bibliometric_analysis.main
python -m bibliometric_analysis.main_radix_sort
python -m bibliometric_analysis.main_bucket_sort
```

El comando instalado `bibliometric-analysis` ejecuta Counting Sort. Cada ejecución imprime los artículos procesados, términos distintos, el tiempo en milisegundos y el top 15 del algoritmo seleccionado.
