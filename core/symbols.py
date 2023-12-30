"""Symbols"""
from dataclasses import dataclass


@dataclass
class Symbol:
    """A representation for musical symbols"""

    simplified: str
    unicode: str
