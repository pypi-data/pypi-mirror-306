from logging import getLogger

from .bibliography_file_extension_enum import BibliographyFileExtensionEnum
from .bibliography_loader import BibliographyLoader
from .bibtex.bibtex_loader import BibTexLoader
from .nbib.nbib_loader import NBibLoader
from .ris.ris_loader import RisLoader
from .exceptions import InvalidBibliographyFileTypeException

logger = getLogger(__name__)


class BibliographyLoaderFactory:

    _bibliography_parser_providers = {
        BibliographyFileExtensionEnum.BIB: BibTexLoader,
        BibliographyFileExtensionEnum.RIS: RisLoader,
        BibliographyFileExtensionEnum.NBIB: NBibLoader,
    }

    def select_bibliography_loader(
        self, bibliography_file_extension: BibliographyFileExtensionEnum
    ) -> BibliographyLoader:

        try:
            bibliography_loader = self._bibliography_parser_providers[
                bibliography_file_extension
            ]()

        except KeyError:

            logger.exception(
                f"File extension {bibliography_file_extension} not supported"
            )

            raise InvalidBibliographyFileTypeException(
                message=f"Bibliography extension {bibliography_file_extension}"
                f" not supported"
            )

        return bibliography_loader
