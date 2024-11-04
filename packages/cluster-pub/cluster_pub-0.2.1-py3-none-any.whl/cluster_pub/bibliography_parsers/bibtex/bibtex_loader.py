from typing import List, Dict
from logging import getLogger

from bibtexparser.bparser import BibTexParser

from .bibtex_entry_parser import parse_bibtex_entry
from ..file_enconding_enum import FileEncodingEnum
from ..bibliography_loader import BibliographyLoader
from ..exceptions import InvalidBibliographyFileException

logger = getLogger(__name__)


class BibTexLoader(BibliographyLoader):

    def __init__(self):
        self.bibtex_parser = BibTexParser(customization=parse_bibtex_entry)

    def load_bibliography_file_entries(self, bibliography_file: str) -> List[Dict]:

        with open(
            file=bibliography_file, encoding=FileEncodingEnum.UTF8
        ) as bibtex_file:

            bibtex_file_data = self.bibtex_parser.parse_file(
                file=bibtex_file, partial=False
            )
            bibtex_file_entries = bibtex_file_data.entries

            if len(bibtex_file_entries) == 0:

                logger.exception(f"File {bibliography_file} is an invalid Bibtex File")

                raise InvalidBibliographyFileException(
                    message=f"Invalid Bibtex File {bibliography_file}"
                )

            return bibtex_file_entries
