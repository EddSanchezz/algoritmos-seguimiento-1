# Análisis de algoritmos en bibliometría

El proyecto procesa los abstracts de 20 artículos científicos en PDF y ordena los términos por frecuencia. El título y los autores se extraen como metadatos, pero no se cuentan.

## Flujo

```text
PDF → extracción del abstract → conteo de términos → pares (término, frecuencia)
   → Counting Sort → tiempo y top 15
```

`main.py` realiza este flujo. Radix Sort y Bucket Sort están disponibles, pero sus imports y llamadas están comentados para ejecutar Counting Sort por ahora.

## Organización del código

```text
data/raw/                              # Los 20 artículos PDF
data/processed/                        # Espacio para resultados generados
src/bibliometric_analysis/
├── pdf_extractor/pdf_extractor.py     # Extracción y validación de abstracts
├── text_processing.py                 # Tokenización y conteo
├── ranking/counting_sort.py           # Counting Sort
├── ranking/radix_sort.py              # Radix Sort
├── ranking/bucket_sort.py             # Bucket Sort
├── main.py                            # Ejecuta Counting Sort
└── cli.py                             # Delega en main.py
```

### Extracción y conteo

`extract_all_from_directory("data/raw")` procesa los PDF y devuelve registros con `id`, `file`, `title`, `authors`, `abstract` y `warnings`. La primera página se usa para localizar la información; se lee todo el documento para reconocer compuestos con guion. El extractor también elimina una referencia incrustada en el abstract del artículo 14.

El conteo usa solamente los abstracts. El texto se convierte a minúsculas, conserva acentos y compuestos como `ai-driven`, omite tokens numéricos y no elimina stopwords. `count_term_frequencies` devuelve un diccionario `{término: frecuencia}`, que `main.py` convierte en pares antes de llamar a los algoritmos.

### Counting Sort

Counting Sort recibe pares `(término, frecuencia)`. Busca la frecuencia máxima, crea una cubeta para cada valor posible y guarda cada par en la cubeta de su frecuencia. Luego recorre las cubetas desde la frecuencia más alta hasta cero. Los términos empatados se conservan en el orden de entrada.

Si `n` es la cantidad de términos distintos y `k` la cantidad de frecuencias posibles (`frecuencia_máxima + 1`), su tiempo y espacio adicional son `O(n + k)`. El algoritmo es conveniente cuando ese rango de frecuencias no es demasiado grande.

## Ejecución

Desde la raíz del proyecto:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
bibliometric-analysis
```

También se puede ejecutar con `python -m bibliometric_analysis.main`. El programa imprime el número de artículos y términos, el tiempo en milisegundos y el top 15 de Counting Sort. El cronómetro mide solo el ordenamiento. No guarda resultados en archivos.
