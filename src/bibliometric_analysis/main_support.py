"""Funciones compartidas por los puntos de entrada de los algoritmos."""

from pathlib import Path

from bibliometric_analysis.pdf_extractor import extract_all_from_directory
from bibliometric_analysis.text_processing import count_term_frequencies

CORPUS_DIRECTORY = Path(__file__).resolve().parents[2] / "data" / "raw"
TOP_TERMS = 15


def load_frequency_pairs() -> list[tuple[str, int]]:
    """Extrae los abstracts y devuelve sus términos con frecuencias."""
    records = extract_all_from_directory(CORPUS_DIRECTORY)
    abstracts = []
    for record in records:
        if record["abstract"]:
            abstracts.append(record["abstract"])

    frequencies = count_term_frequencies(abstracts)
    print(f"Artículos procesados: {len(records)}")
    print(f"Abstracts con texto: {len(abstracts)}")
    print(f"Términos distintos: {len(frequencies)}")
    return list(frequencies.items())


def print_ranking(
    algorithm_name: str,
    ranking: list[tuple[str, int]],
    elapsed_ms: float,
) -> None:
    """Muestra el tiempo y los 15 términos principales."""
    print(f"\n{algorithm_name}: {elapsed_ms:.3f} ms")
    position = 1
    for term, frequency in ranking[:TOP_TERMS]:
        print(f"{position:>2}. {term:<22} {frequency}")
        position += 1
