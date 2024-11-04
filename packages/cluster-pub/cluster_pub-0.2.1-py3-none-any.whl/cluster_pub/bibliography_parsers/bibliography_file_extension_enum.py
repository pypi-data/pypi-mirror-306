from enum import Enum


class BibliographyFileExtensionEnum(str, Enum):
    BIB: str = "bib"
    RIS: str = "ris"
    NBIB: str = "nbib"
