"""Bucket Sort para ordenar frecuencias de terminos y generar el ranking."""

import sys
import time
from collections.abc import Iterable
from pathlib import Path

from bibliometric_analysis.pdf_extractor import extract_all_from_directory
from bibliometric_analysis.text_processing import count_term_frequencies

DEFAULT_CORPUS_DIRECTORY = Path(__file__).resolve().parents[3] / "data" / "raw"
DEFAULT_TOP_TERMS = 15

FrequencyPair = tuple[str, int]


def run_bucket_sort(
    corpus_directory: Path = DEFAULT_CORPUS_DIRECTORY,
    top: int = DEFAULT_TOP_TERMS,
) -> None:
    """Extrae el corpus, cuenta terminos y muestra el top con Bucket Sort."""
    if top < 1:
        raise ValueError("La cantidad de terminos debe ser mayor que cero")

    documents = _extract_documents(corpus_directory)
    abstracts = [document["abstract"] for document in documents if document.get("abstract")]
    _warn_missing_abstracts(documents)

    frequencies = count_term_frequencies(abstracts)
    pairs = list(frequencies.items())

    start = time.perf_counter()
    ordered = bucket_sort(pairs)
    elapsed_ms = (time.perf_counter() - start) * 1000
    ranking = ordered[:top]

    print(f"Documentos procesados: {len(documents)}")
    print(f"Abstracts con texto: {len(abstracts)}")
    print(f"Terminos unicos: {len(frequencies)}")
    print(f"Tiempo de ordenamiento (Bucket Sort): {elapsed_ms:.3f} ms")
    print()
    print(f"Top {len(ranking)} terminos mas frecuentes (Bucket Sort):")
    for position, (term, frequency) in enumerate(ranking, start=1):
        print(f"{position:>3}. {term:<20} {frequency:>5}")


def bucket_sort(
    pairs: Iterable[FrequencyPair],
    num_buckets: int | None = None,
) -> list[FrequencyPair]:
    """Ordena pares (termino, frecuencia) de mayor a menor con Bucket Sort.

    Los pares se distribuyen en cubetas segun su frecuencia. Por defecto se
    usa una cubeta por cada frecuencia entera posible (``k = max_freq``), de
    modo que cada cubeta agrupa terminos con la misma frecuencia. Luego cada
    cubeta se ordena con insertion sort y se concatenan de mayor a menor.

    No se aplica desempate: los pares con igual frecuencia conservan el orden
    en que aparecen en la entrada. La lista original no se modifica.

    Args:
        pairs: Pares ``(termino, frecuencia)`` con frecuencias no negativas.
        num_buckets: Cantidad de cubetas. Si es ``None`` se usa ``max_freq``.
            Valores fuera del rango valido se ajustan a ``[1, max_freq]``.

    Returns:
        Nueva lista de pares ordenada por frecuencia descendente.

    Complejidad:
        ``n`` es el numero de pares y ``k`` el numero de cubetas. Distribuir
        cuesta ``O(n)`` y concatenar ``O(n + k)``. El insertion sort de cada
        cubeta cuesta ``O(b_i^2)`` en el peor caso, por lo que el total es
        ``O(n + k + sum(b_i^2))``. Con ``k = max_freq`` cada cubeta contiene
        frecuencias iguales y el costo interno es lineal, quedando
        ``O(n + max_freq)`` para este corpus.
    """
    items = [(term, frequency) for term, frequency in pairs]
    if not items:
        return []

    if any(frequency < 0 for _, frequency in items):
        raise ValueError("Las frecuencias no pueden ser negativas")

    max_frequency = max(frequency for _, frequency in items)
    bucket_count = _resolve_bucket_count(max_frequency, num_buckets)

    buckets: list[list[FrequencyPair]] = [[] for _ in range(bucket_count)]
    for term, frequency in items:
        index = (frequency * (bucket_count - 1)) // max_frequency if max_frequency else 0
        buckets[index].append((term, frequency))

    ordered: list[FrequencyPair] = []
    for bucket in reversed(buckets):
        _insertion_sort_descending(bucket)
        ordered.extend(bucket)
    return ordered


def _extract_documents(corpus_directory: Path) -> list[dict]:
    """Extrae todos los PDFs del corpus y los ordena por nombre de archivo."""
    if not corpus_directory.is_dir():
        raise FileNotFoundError(f"No existe el directorio del corpus: {corpus_directory}")
    documents = extract_all_from_directory(str(corpus_directory))
    return sorted(
        documents,
        key=lambda document: str(document.get("file") or document.get("archivo", "")),
    )


def _warn_missing_abstracts(documents: list[dict]) -> None:
    """Avisa por stderr cuando un documento no tiene abstract extraible."""
    for document in documents:
        if not document.get("abstract"):
            file_name = document.get("file") or document.get("archivo", "documento")
            print(
                f"Aviso: no se pudo extraer el abstract de {file_name}",
                file=sys.stderr,
            )


def _resolve_bucket_count(max_frequency: int, num_buckets: int | None) -> int:
    """Calcula una cantidad de cubetas valida para el rango de frecuencias."""
    if max_frequency <= 0:
        return 1
    if num_buckets is None:
        return max_frequency
    return max(1, min(num_buckets, max_frequency))


def _insertion_sort_descending(pairs: list[FrequencyPair]) -> None:
    """Ordena una cubeta por frecuencia de mayor a menor, sin desempate."""
    for position in range(1, len(pairs)):
        current = pairs[position]
        previous = position - 1
        while previous >= 0 and pairs[previous][1] < current[1]:
            pairs[previous + 1] = pairs[previous]
            previous -= 1
        pairs[previous + 1] = current
