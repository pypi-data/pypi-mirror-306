from abc import abstractmethod
from typing import List, Dict

from .schemas import BibliographyFileData


class BibliographyLoader:

    def load_bibliography_file(
        self, bibliography_file: str
    ) -> List[BibliographyFileData]:

        bibliography_file_entries = self.load_bibliography_file_entries(
            bibliography_file=bibliography_file
        )

        serialized_bibliography_file_content = list(
            self.serialize_bibliography_entry(
                bibliography_entry=bibliography_file_entry
            )
            for bibliography_file_entry in bibliography_file_entries
        )

        return serialized_bibliography_file_content

    @abstractmethod
    def load_bibliography_file_entries(self, bibliography_file: str) -> List[Dict]:
        raise NotImplementedError()

    def serialize_bibliography_entry(
        self, bibliography_entry: Dict
    ) -> BibliographyFileData:

        bibliography_entry_title = bibliography_entry.get("title")
        bibliography_entry_abstract = (
            bibliography_entry.get("abstract") or bibliography_entry_title
        )

        serialized_bibliography_entry = BibliographyFileData(
            title=bibliography_entry_title, abstract=bibliography_entry_abstract
        )

        return serialized_bibliography_entry
