"""Conteo de terminos en abstracts extraidos y normalizados."""

import re
import unicodedata
from collections import Counter
from collections.abc import Iterable

TOKEN_PATTERN = re.compile(r"[^\W\d_]+(?:[-'’][^\W\d_]+)*", re.UNICODE)


def tokenize_text(text: str) -> list[str]:
    """Separa palabras, conserva acentos y compuestos, y omite numeros."""
    normalized_text = unicodedata.normalize("NFC", text.lower())
    return TOKEN_PATTERN.findall(normalized_text)


def count_term_frequencies(abstracts: Iterable[str | None]) -> dict[str, int]:
    """Cuenta terminos en abstracts normalizados; ignora los vacios y None."""
    frequencies: Counter[str] = Counter()
    for abstract in abstracts:
        if abstract:
            frequencies.update(tokenize_text(abstract))
    return dict(frequencies)
