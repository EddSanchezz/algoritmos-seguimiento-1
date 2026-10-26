"""Punto de entrada de la interfaz de linea de comandos."""

from bibliometric_analysis.ranking.bucket_sort import run_bucket_sort


def main() -> None:
    """Ejecuta el ranking de terminos del corpus con Bucket Sort."""
    run_bucket_sort()


if __name__ == "__main__":
    main()
