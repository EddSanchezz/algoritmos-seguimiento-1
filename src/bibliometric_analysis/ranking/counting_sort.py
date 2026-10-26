"""Counting Sort para ordenar terminos por frecuencia."""


def counting_sort(items: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Ordena pares (termino, frecuencia) de mayor a menor frecuencia.

    Las frecuencias deben ser enteros no negativos. Si hay empates, conserva
    el orden que tenian los terminos en la entrada.
    """
    if not items:
        return []

    max_frequency = 0
    for item in items:
        frequency = item[1]
        if frequency < 0:
            raise ValueError("Las frecuencias no pueden ser negativas")
        if frequency > max_frequency:
            max_frequency = frequency

    buckets = []
    frequency = 0
    while frequency <= max_frequency:
        buckets.append([])
        frequency += 1

    for item in items:
        frequency = item[1]
        buckets[frequency].append(item)

    ordered_items = []
    frequency = max_frequency
    while frequency >= 0:
        for item in buckets[frequency]:
            ordered_items.append(item)
        frequency -= 1

    return ordered_items
