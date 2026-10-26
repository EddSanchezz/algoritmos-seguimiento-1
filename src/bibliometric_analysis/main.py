"""Punto de entrada para ejecutar el ranking con Bucket Sort."""

from bibliometric_analysis.ranking.bucket_sort import run_bucket_sort


def main() -> None:
    """Ejecuta la extraccion, el conteo y el ranking del corpus."""
    run_bucket_sort()


if __name__ == "__main__":
    main()
