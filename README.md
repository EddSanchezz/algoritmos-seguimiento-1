# Análisis de algoritmos en bibliometría

Proyecto académico del Seguimiento 2026-2. Procesa los abstracts de 20 artículos científicos y genera rankings de términos frecuentes. El título y los autores se extraen como metadatos, pero no se cuentan.

El documento del seguimiento solicita implementar Counting Sort, Radix Sort y Bucket Sort, explicar sus complejidades, medir los tiempos en milisegundos y presentar el top 15 de cada algoritmo. Este README explica el flujo del proyecto y desarrolla Counting Sort; Radix Sort y Bucket Sort son implementaciones de otros integrantes.

## Estructura

```text
data/
├── raw/                         # Los 20 artículos en PDF
└── processed/                   # Espacio reservado para resultados generados
src/bibliometric_analysis/
├── pdf_extractor/
│   ├── __init__.py
│   └── pdf_extractor.py         # Extracción y validación de abstracts
├── ranking/
│   ├── __init__.py
│   ├── counting_sort.py         # Implementación explicada en este README
│   ├── radix_sort.py            # Implementación de otro integrante
│   └── bucket_sort.py           # Implementación de otro integrante
├── text_processing.py           # Tokenización y conteo
├── main.py                      # Entrada principal actual
└── cli.py                       # Comando configurado en pyproject.toml
```

## Flujo de los datos

1. `extract_all_from_directory("data/raw")` procesa los PDF en orden y devuelve un registro por archivo.
2. Cada registro contiene `id`, `file`, `title`, `authors`, `abstract` y `warnings`. Solo el abstract pasa al conteo.
3. `count_term_frequencies` tokeniza los abstracts y devuelve un diccionario `{termino: frecuencia}`.
4. `list(frequencies.items())` crea los pares `(termino, frecuencia)` que reciben los algoritmos de ranking.
5. Counting Sort devuelve los pares ordenados de mayor a menor frecuencia. Se puede tomar `ranking[:15]` para obtener su top 15.

## Extracción de PDF

El código está en `src/bibliometric_analysis/pdf_extractor/pdf_extractor.py` y usa `pdfplumber`.

- `extract_pdf(path)` extrae un PDF; `extract_all_from_directory(path)` procesa los PDF de una carpeta.
- La primera página se usa para localizar título, autores y abstract. También se leen las páginas del documento para construir el vocabulario que ayuda a distinguir cortes de línea de compuestos reales.
- Se reconstruyen las líneas del abstract, se corrigen los cortes de palabra y se conserva el guion cuando corresponde a un compuesto presente en el documento, por ejemplo `instance-based` o `ai-driven`.
- Los abstracts quedan en minúsculas y se conservan sus acentos. El PDF 14 contiene una referencia incrustada en el abstract; el extractor la elimina.
- `validate_extraction(records)` comprueba que estén los 20 registros, que tengan abstract y que su longitud y formato sean razonables.

La extracción completa puede tardar alrededor de un minuto y medio porque el vocabulario se construye leyendo todas las páginas. Los PDF deben tener una capa de texto; los PDF escaneados pueden requerir OCR, que no está implementado.

Ejemplo:

```python
from bibliometric_analysis.pdf_extractor import extract_all_from_directory
from bibliometric_analysis.pdf_extractor.pdf_extractor import validate_extraction

records = extract_all_from_directory("data/raw")
problems = validate_extraction(records)
print(problems)
```

## Normalización y conteo

`src/bibliometric_analysis/text_processing.py` contiene dos funciones:

- `tokenize_text(text)` separa palabras y conserva letras acentuadas, guiones y apóstrofes internos. Pasa los términos a minúsculas y no incluye tokens formados solo por números.
- `count_term_frequencies(abstracts)` cuenta las apariciones en todos los abstracts y devuelve un diccionario de frecuencias.

No se eliminan stopwords ni se aplican stemming o lematización. Los compuestos como `ai-driven` se cuentan como un término.

## Counting Sort

Archivo: `src/bibliometric_analysis/ranking/counting_sort.py`.

### Entrada y salida

Recibe una lista de pares `(termino, frecuencia)` con frecuencias enteras no negativas y devuelve una nueva lista ordenada de mayor a menor. No modifica la lista original. Si la entrada está vacía, devuelve `[]`.

```python
from bibliometric_analysis.ranking import counting_sort

items = [("ai", 2), ("education", 1), ("model", 2)]
print(counting_sort(items))
# [('ai', 2), ('model', 2), ('education', 1)]
```

Los términos empatados se guardan en la misma cubeta. Como se agregan y se recuperan en orden, se conserva entre ellos el orden de entrada; no se agrega un desempate alfabético.

### Idea del algoritmo

1. Busca la frecuencia máxima.
2. Crea una lista de cubetas: el índice de cada cubeta representa una frecuencia posible.
3. Guarda cada par en la cubeta indicada por su frecuencia.
4. Recorre las cubetas desde la frecuencia máxima hasta cero y concatena sus elementos.

El algoritmo no compara los pares entre sí: usa la frecuencia como índice. Si hay `n` términos distintos y `k` frecuencias posibles desde cero hasta la máxima, el tiempo y el espacio adicional son `O(n + k)`. En particular, `k = frecuencia_máxima + 1`; por eso el algoritmo es conveniente cuando ese rango no es desproporcionadamente grande.

### Ejecutar Counting Sort sobre el corpus

La medición siguiente incluye únicamente la llamada al algoritmo; extracción y conteo quedan fuera del cronómetro:

```python
from time import perf_counter

from bibliometric_analysis.pdf_extractor import extract_all_from_directory
from bibliometric_analysis.text_processing import count_term_frequencies
from bibliometric_analysis.ranking import counting_sort

records = extract_all_from_directory("data/raw")
abstracts = [record["abstract"] for record in records if record["abstract"]]
frequencies = count_term_frequencies(abstracts)
items = list(frequencies.items())

start = perf_counter()
ranking = counting_sort(items)
elapsed_ms = (perf_counter() - start) * 1000

print(f"Tiempo de Counting Sort: {elapsed_ms:.3f} ms")
for position, (term, frequency) in enumerate(ranking[:15], start=1):
    print(f"{position:>2}. {term:<20} {frequency}")
```

## Ejecución del proyecto

Instalar en un entorno virtual desde la raíz del proyecto:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
```

El comando `bibliometric-analysis` y `main.py` actualmente delegan la ejecución al flujo de Bucket Sort. Para ejecutar y medir Counting Sort individualmente, usa el ejemplo de la sección anterior. No se alteró la implementación de Radix Sort ni Bucket Sort.

## Módulos principales

| Módulo | Responsabilidad |
| --- | --- |
| `pdf_extractor/pdf_extractor.py` | Extraer, limpiar y validar información de los PDF. |
| `text_processing.py` | Tokenizar abstracts y contar términos. |
| `ranking/counting_sort.py` | Ordenar pares por frecuencia mediante cubetas indexadas. |
| `ranking/radix_sort.py` | Implementación de Radix Sort a cargo de otro integrante. |
| `ranking/bucket_sort.py` | Implementación de Bucket Sort a cargo de otro integrante. |
| `main.py`, `cli.py` | Entradas actuales del programa, conectadas al flujo de Bucket Sort. |

Los archivos generados pertenecen a `data/processed/`. No se incluyen carpetas de `tests/` ni `reports/` en la estructura actual.
