"""Parsers module init file."""

from .pdf_parser import PDFParser
from .docx_parser import DOCXParser
from .txt_parser import TXTParser

__all__ = ['PDFParser', 'DOCXParser', 'TXTParser']
