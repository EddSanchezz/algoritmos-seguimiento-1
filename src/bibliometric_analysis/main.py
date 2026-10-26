"""Punto de entrada para ejecutar Counting Sort."""

from time import perf_counter

from bibliometric_analysis.main_support import load_frequency_pairs, print_ranking
from bibliometric_analysis.ranking.counting_sort import counting_sort


def main() -> None:
    """Ejecuta Counting Sort sobre los abstracts del corpus."""
    items = load_frequency_pairs()

    start = perf_counter()
    ranking = counting_sort(items)
    elapsed_ms = (perf_counter() - start) * 1000

    print_ranking("Counting Sort", ranking, elapsed_ms)


if __name__ == "__main__":
    main()
