"""Ejecuta los algoritmos de ordenamiento sobre el corpus."""

from pathlib import Path
from time import perf_counter

from bibliometric_analysis.pdf_extractor import extract_all_from_directory
from bibliometric_analysis.ranking.counting_sort import counting_sort
from bibliometric_analysis.text_processing import count_term_frequencies
# from bibliometric_analysis.ranking.radix_sort import radix_sort
# from bibliometric_analysis.ranking.bucket_sort import bucket_sort

CORPUS_DIRECTORY = Path(__file__).resolve().parents[2] / "data" / "raw"
TOP_TERMS = 15


def main() -> None:
    """Extrae abstracts, cuenta terminos y muestra el top 15 de cada algoritmo."""
    records = extract_all_from_directory(CORPUS_DIRECTORY)

    abstracts = []
    for record in records:
        if record["abstract"]:
            abstracts.append(record["abstract"])

    frequencies = count_term_frequencies(abstracts)
    items = list(frequencies.items())

    start = perf_counter()
    counting_ranking = counting_sort(items)
    counting_time = (perf_counter() - start) * 1000

    print(f"Articulos procesados: {len(records)}")
    print(f"Abstracts con texto: {len(abstracts)}")
    print(f"Terminos distintos: {len(frequencies)}")

    print(f"\nCounting Sort — {counting_time:.3f} ms")
    position = 1
    for term, frequency in counting_ranking[:TOP_TERMS]:
        print(f"{position:>2}. {term:<22} {frequency}")
        position += 1

    # radix_ranking = radix_sort(items)
    # bucket_ranking = bucket_sort(items)


if __name__ == "__main__":
    main()
