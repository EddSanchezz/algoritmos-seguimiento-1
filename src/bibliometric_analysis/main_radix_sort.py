"""Punto de entrada para ejecutar Radix Sort."""

from time import perf_counter

from bibliometric_analysis.main_support import load_frequency_pairs, print_ranking
from bibliometric_analysis.ranking.radix_sort import radix_sort


def main() -> None:
    """Ejecuta Radix Sort sobre los abstracts del corpus."""
    items = load_frequency_pairs()

    start = perf_counter()
    ranking = radix_sort(items)
    elapsed_ms = (perf_counter() - start) * 1000

    print_ranking("Radix Sort", ranking, elapsed_ms)


if __name__ == "__main__":
    main()
