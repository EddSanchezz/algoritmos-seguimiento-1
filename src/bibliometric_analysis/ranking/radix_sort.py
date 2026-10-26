"""Radix Sort para ordenar frecuencias de terminos."""


def counting_sort_by_digit(
    items: list[tuple[str, int]], exp: int
) -> list[tuple[str, int]]:
    """Ordena los pares (termino, frecuencia) segun el digito en la posicion exp.

    Funciona como la subrutina estable de ordenamiento por conteo para Radix Sort.
    """
    n = len(items)
    output = [None] * n

    # Base 10: un contador para cada digito del 0 al 9
    count = [0] * 10

    # Contar cuantas veces aparece cada digito en la posicion actual
    for item in items:
        freq = item[1]
        digit = (freq // exp) % 10
        count[digit] += 1

    # Suma acumulada para determinar la posicion final de cada elemento
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Recorrer de atras hacia adelante para mantener la estabilidad del ordenamiento
    for i in range(n - 1, -1, -1):
        item = items[i]
        freq = item[1]
        digit = (freq // exp) % 10
        pos = count[digit] - 1
        output[pos] = item
        count[digit] -= 1

    return output


def radix_sort(
    items: list[tuple[str, int]], descending: bool = True
) -> list[tuple[str, int]]:
    """Ordena una lista de pares (termino, frecuencia) usando Radix Sort (LSD).

    Args:
        items: Lista de tuplas con formato (termino, frecuencia).
        descending: True para ranking (mayor a menor frecuencia), False para ascendente.
    """
    result = list(items)

    if len(result) <= 1:
        return result

    # Validacion: las frecuencias no pueden ser negativas
    for _, freq in result:
        if freq < 0:
            raise ValueError("Las frecuencias no pueden ser negativas")

    # Buscar la frecuencia mas alta para saber cuantos digitos procesar
    max_freq = max(item[1] for item in result)
    if max_freq == 0:
        return result

    # Procesar digito por digito: unidades (1), decenas (10), centenas (100)...
    exp = 1
    while max_freq // exp > 0:
        result = counting_sort_by_digit(result, exp)
        exp *= 10

    # Radix ordena de menor a mayor; para el ranking se invierte de mayor a menor
    if descending:
        result.reverse()

    return result
