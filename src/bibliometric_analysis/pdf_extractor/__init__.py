"""Paquete de extracción de información de PDFs."""
from .pdf_extractor import extract_pdf, extract_all_from_directory

__all__ = ["extract_pdf", "extract_all_from_directory"]