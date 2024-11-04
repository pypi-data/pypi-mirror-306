from typing import List, Dict
from logging import getLogger

from rispy import load
from rispy.parser import ParseError

from ..file_enconding_enum import FileEncodingEnum
from ..bibliography_loader import BibliographyLoader
from ..exceptions import InvalidBibliographyFileException

logger = getLogger(__name__)


class RisLoader(BibliographyLoader):

    def load_bibliography_file_entries(self, bibliography_file: str) -> List[Dict]:

        utf8_encoding = FileEncodingEnum.UTF8

        with open(file=bibliography_file, encoding=utf8_encoding) as ris_file:

            try:
                ris_file_entries = load(file=ris_file, encoding=utf8_encoding)

            except ParseError:

                logger.exception(f"File {bibliography_file} is an Invalid Ris File")

                raise InvalidBibliographyFileException(
                    message=f"Invalid Ris File {bibliography_file}"
                )

            return ris_file_entries
