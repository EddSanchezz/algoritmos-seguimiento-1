"""Counting Sort para ordenar terminos por frecuencia."""


def counting_sort(items: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Ordena pares (termino, frecuencia) de mayor a menor frecuencia.

    Las frecuencias deben ser enteros no negativos. Si hay empates, conserva
    el orden que tenian los terminos en la entrada.
    """
    if not items:
        return []

    for _, frequency in items:
        if frequency < 0:
            raise ValueError("Las frecuencias no pueden ser negativas")

    max_frequency = max(frequency for _, frequency in items)
    buckets = [[] for _ in range(max_frequency + 1)]

    for item in items:
        buckets[item[1]].append(item)

    ordered_items = []
    for frequency in range(max_frequency, -1, -1):
        ordered_items.extend(buckets[frequency])

    return ordered_items
