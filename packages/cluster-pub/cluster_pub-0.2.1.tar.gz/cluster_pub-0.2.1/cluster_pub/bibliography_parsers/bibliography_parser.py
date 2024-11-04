from typing import List
from time import time
from logging import getLogger

from .schemas import BibliographyFileData
from .bibliography_file_extension_enum import BibliographyFileExtensionEnum
from .bibliography_loader_factory import BibliographyLoaderFactory

logger = getLogger(__name__)


class BibliographyParser:

    def __init__(self):
        self.bibliography_loader_factory = BibliographyLoaderFactory()

    def parse_bibliography_file(
        self, bibliography_file: str
    ) -> List[BibliographyFileData]:

        initial_time = time()

        logger.info(f"Starting to parse bibliography file {bibliography_file}")

        bibliography_file_extension = self.get_bibliography_file_extension(
            bibliography_file=bibliography_file
        )

        bibliography_loader = (
            self.bibliography_loader_factory.select_bibliography_loader(
                bibliography_file_extension=bibliography_file_extension
            )
        )

        parsed_bibliography_file_content = bibliography_loader.load_bibliography_file(
            bibliography_file=bibliography_file
        )

        finish_time = time() - initial_time
        logger.info(f"Time to parse file {bibliography_file}: {finish_time}")

        logger.info(
            f"Parsed {len(parsed_bibliography_file_content)} entries from bibliography file {bibliography_file}"
        )

        return parsed_bibliography_file_content

    def get_bibliography_file_extension(
        self, bibliography_file: str
    ) -> BibliographyFileExtensionEnum:

        bibliography_file_extensions = bibliography_file.split(".")

        bibliography_file_extension = bibliography_file_extensions[-1]

        return bibliography_file_extension
