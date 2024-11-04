import re
from typing import List
from multiprocessing import cpu_count, Pool
from time import time
from unicodedata import normalize
from logging import getLogger

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from ..bibliography_parsers.schemas import BibliographyFileData
from .schemas import ProcessedBibliographyFileData

logger = getLogger(__name__)


class BibliographyAbstractProcessor:

    _numbers_to_letter_mapping = str.maketrans("0123456789", "ABCDEFGHIJ")
    _stop_words = ENGLISH_STOP_WORDS

    def process_bibliography_file_entries(
        self, bibliography_file_entries: List[BibliographyFileData]
    ) -> List[ProcessedBibliographyFileData]:
        initial_time = time()

        logger.info("Starting to pre-process bibliography entries content")

        with Pool(processes=cpu_count()) as process_executor:

            processed_bibliography_file_results = process_executor.map(
                self.process_bibliography_file_entry,
                bibliography_file_entries,
                chunksize=50,
            )

        finish_time = time() - initial_time
        logger.info(f"Time to pre-process entries: {finish_time}")

        logger.info("Pre-processed entries successfully")

        return processed_bibliography_file_results

    def process_bibliography_file_entry(
        self, bibliography_file_entry: BibliographyFileData
    ) -> ProcessedBibliographyFileData:

        processed_bibliography_abstract = self.process_bibliography_abstract(
            bibliography_abstract=bibliography_file_entry["abstract"]
        )

        processed_bibliography_file_entry = ProcessedBibliographyFileData(
            title=bibliography_file_entry["title"],
            processed_abstract=processed_bibliography_abstract,
        )

        return processed_bibliography_file_entry

    def process_bibliography_abstract(self, bibliography_abstract: str) -> str:

        abstract_without_stop_words = self.remove_abstract_stop_words(
            abstract=bibliography_abstract
        )

        filtered_bibliography_abstract = re.sub(
            r"[^a-zA-Z0-9]", str(), abstract_without_stop_words
        )

        decoded_bibliography_abstract = self.decode_abstract(
            abstract=filtered_bibliography_abstract
        )

        processed_bibliography_abstract = decoded_bibliography_abstract.translate(
            self._numbers_to_letter_mapping
        )

        return processed_bibliography_abstract.upper()

    def decode_abstract(self, abstract: str) -> str:
        initially_decoded_abstract = normalize("NFKD", abstract)
        bytes_processed_abstract = initially_decoded_abstract.encode("ascii", "ignore")

        decoded_abstract = bytes_processed_abstract.decode("UTF-8")

        return decoded_abstract

    def remove_abstract_stop_words(self, abstract: str) -> str:

        lower_abstract = abstract.lower()
        abstract_words = lower_abstract.split(" ")

        filtered_abstract_words = list(
            abstract_word
            for abstract_word in abstract_words
            if abstract_word not in self._stop_words
        )
        filtered_abstract = str().join(filtered_abstract_words)

        return filtered_abstract
