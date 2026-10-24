# pdf_extractor

## Propósito

Extrae título, autores y abstract de artículos científicos en formato PDF.

## Funciones principales

### `extract_pdf(pdf_path)`

Extrae información de un solo archivo PDF.

**Parámetros:**
- `pdf_path` (str): Ruta al archivo PDF

**Retorna:** `dict` con las siguientes claves:
- `archivo` (str): Ruta del archivo procesado
- `titulo` (str): Título del artículo
- `autores` (str): Autores del artículo
- `abstract` (str): Resumen/abstract del artículo
- `aviso` (str, opcional): Advertencia si el PDF no tiene texto extraíble

### `extract_all_from_directory(directory_path)`

Extrae información de todos los PDFs en un directorio.

**Parámetros:**
- `directory_path` (str): Ruta al directorio que contiene los PDFs

**Retorna:** `list[dict]`: Lista de diccionarios con la información de cada PDF

## Ejemplo de uso

```python
from src.bibliometric_analysis.pdf_extractor import extract_pdf

# Extraer de un PDF individual
result = extract_pdf("data/raw/1. Artificial intelligence literacy.pdf")
print(result["titulo"])
print(result["autores"])
print(result["abstract"])

# Extraer de todos los PDFs en un directorio
from src.bibliometric_analysis.pdf_extractor import extract_all_from_directory

results = extract_all_from_directory("data/raw/")
for r in results:
    print(f"{r['archivo']}: {r['titulo'][:50]}...")
```

## Dependencias

Requiere `pdfplumber`. Instalar con:
```powershell
pip install pdfplumber
```

## Notas

- Procesa solo la primera página del PDF (donde generalmente están título, autores y abstract)
- Funciona con PDFs que tengan capa de texto (no escaneados)
- El título se extrae basándose en tamaño de fuente mayor al cuerpo
- El abstract se detecta buscando el encabezado "Abstract" o similar