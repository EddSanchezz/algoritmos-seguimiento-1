"""Conteo de terminos en abstracts extraidos y normalizados."""

import re
import unicodedata
from collections import Counter
from collections.abc import Iterable

TOKEN_PATTERN = re.compile(r"[^\W\d_]+(?:[-'’][^\W\d_]+)*", re.UNICODE)
STOP_WORDS = {
    "a", "about", "after", "again", "against", "all", "also", "am", "an",
    "and", "any", "are", "as", "at", "be", "because", "been", "before",
    "being", "below", "between", "both", "but", "by", "can", "could",
    "did", "do", "does", "doing", "down", "during", "each", "few", "for",
    "from", "further", "had", "has", "have", "having", "he", "her", "here",
    "hers", "him", "his", "how", "i", "if", "in", "into", "is", "it", "its",
    "just", "me", "more", "most", "my", "no", "nor", "not", "now", "of",
    "off", "on", "once", "only", "or", "other", "our", "ours", "out", "over",
    "own", "same", "she", "should", "so", "some", "such", "than", "that",
    "the", "their", "them", "then", "there", "these", "they", "this", "those",
    "through", "to", "too", "under", "until", "up", "very", "was", "we",
    "were", "what", "when", "where", "which", "while", "who", "whom", "why",
    "with", "would", "you", "your",
}


def tokenize_text(text: str) -> list[str]:
    """Separa términos y omite números y palabras conectoras comunes."""
    normalized_text = unicodedata.normalize("NFC", text.lower())
    words = TOKEN_PATTERN.findall(normalized_text)

    terms = []
    for word in words:
        if word not in STOP_WORDS:
            terms.append(word)

    return terms


def count_term_frequencies(abstracts: Iterable[str | None]) -> dict[str, int]:
    """Cuenta terminos en abstracts normalizados; ignora los vacios y None."""
    frequencies: Counter[str] = Counter()
    for abstract in abstracts:
        if abstract:
            frequencies.update(tokenize_text(abstract))
    return dict(frequencies)
