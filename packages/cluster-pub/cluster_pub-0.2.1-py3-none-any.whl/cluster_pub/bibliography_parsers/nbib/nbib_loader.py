from typing import List, Dict
from logging import getLogger

from nbib import read
from nbib.exceptions import MalformedLine, UnknownTagFormat

from ..bibliography_loader import BibliographyLoader
from ..file_enconding_enum import FileEncodingEnum
from ..exceptions import InvalidBibliographyFileException

logger = getLogger(__name__)


class NBibLoader(BibliographyLoader):

    def load_bibliography_file_entries(self, bibliography_file: str) -> List[Dict]:

        with open(file=bibliography_file, encoding=FileEncodingEnum.UTF8) as nbib_file:

            nbib_file_content = nbib_file.read()

            try:
                nbib_file_entries = read(content=nbib_file_content)

            except (MalformedLine, UnknownTagFormat):

                logger.exception(f"File {bibliography_file} is an Invalid NBIB File")

                raise InvalidBibliographyFileException(
                    message=f"Invalid NBIB File {bibliography_file}"
                )

            return nbib_file_entries
