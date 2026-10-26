"""Funciones de normalizacion y conteo de texto del corpus."""

import re
import unicodedata
from collections import Counter
from collections.abc import Iterable

TOKEN_PATTERN = re.compile(r"[^\W_]+", re.UNICODE)


def remove_diacritics(text: str) -> str:
    """Quita los diacriticos del texto conservando la letra enie."""
    protected = text.replace("ñ", "\x00")
    decomposed = unicodedata.normalize("NFD", protected)
    without_marks = "".join(
        character for character in decomposed if unicodedata.category(character) != "Mn"
    )
    return without_marks.replace("\x00", "ñ")


def normalize_text(text: str, normalize: bool = True) -> str:
    """Normaliza el texto segun la opcion acordada.

    Con ``normalize=True`` convierte a minusculas y quita diacriticos sin
    eliminar la enie. Con ``normalize=False`` respeta mayusculas y diacriticos.
    """
    if not normalize:
        return text

    lowered = unicodedata.normalize("NFKC", text).lower()
    return remove_diacritics(lowered)


def tokenize_text(text: str, normalize: bool = True) -> list[str]:
    """Separa el texto en terminos, quitando la puntuacion.

    No se eliminan palabras comunes: solo se separan de los signos.
    """
    return TOKEN_PATTERN.findall(normalize_text(text, normalize=normalize))


def count_terms(text: str, normalize: bool = True) -> Counter[str]:
    """Cuenta las frecuencias de los terminos de un solo texto."""
    return Counter(tokenize_text(text, normalize=normalize))


def count_term_frequencies(
    abstracts: Iterable[str | None], normalize: bool = True
) -> dict[str, int]:
    """Cuenta las frecuencias de los terminos de un conjunto de abstracts.

    Los abstracts vacios o no disponibles se ignoran. El resultado es un
    diccionario ``termino -> frecuencia`` con el que se construye el ranking.
    """
    frequencies: Counter[str] = Counter()
    for abstract in abstracts:
        if abstract:
            frequencies.update(count_terms(abstract, normalize=normalize))
    return dict(frequencies)
