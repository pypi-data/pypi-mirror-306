from numpy import array
from rich.progress import Progress

from cluster_pub.bibliography_parsers.bibliography_parser import BibliographyParser
from cluster_pub.bibliography_abstract_processor.bibliography_abstract_processor import (
    BibliographyAbstractProcessor,
)
from cluster_pub.abstract_embedder.abstract_embedder import AbstractEmbedder
from cluster_pub.abstract_similarity_calculator.abstract_similarity_calculator import (
    AbstractSimilarityCalculator,
)
from cluster_pub.dendogram_builder.dendogram_builder import DendogramBuilder


class ClusterPub:

    def __init__(self):
        self.bibliography_parser = BibliographyParser()
        self.bibliography_processor = BibliographyAbstractProcessor()
        self.abstract_embedder = AbstractEmbedder()
        self.similarity_calculator = AbstractSimilarityCalculator()
        self.dendogram_builder = DendogramBuilder()

    def cluster_publications(
        self,
        source_bibliography_file: str,
        result_file: str,
        progress_manager: Progress,
    ):

        parse_file_task_id = progress_manager.add_task(
            description=f"Parsing bibliographic file {source_bibliography_file}",
            total=None,
        )
        parsed_bibliography_entries = self.bibliography_parser.parse_bibliography_file(
            bibliography_file=source_bibliography_file
        )
        progress_manager.update(task_id=parse_file_task_id, visible=False)
        progress_manager.print(
            f"[green]Parsed bibliographic file {source_bibliography_file} ✓ "
        )

        preprocess_entries_task_id = progress_manager.add_task(
            description="Pre-processing file entries", total=None
        )
        processed_bibliography_entries = (
            self.bibliography_processor.process_bibliography_file_entries(
                bibliography_file_entries=parsed_bibliography_entries
            )
        )
        progress_manager.update(task_id=preprocess_entries_task_id, visible=False)
        progress_manager.print("[green]Pre-processed bibliographic file entries ✓")

        embed_abstracts_task_id = progress_manager.add_task(
            description="Embedding abstracts", total=None
        )
        embedded_abstracts = self.abstract_embedder.embed_bibliography_abstracts(
            bibliography_abstracts=processed_bibliography_entries
        )
        progress_manager.update(task_id=embed_abstracts_task_id, visible=False)
        progress_manager.print("[green]Embedded bibliographic abstracts ✓")

        cluster_publications_task_id = progress_manager.add_task(
            description="Clustering publications", total=None
        )
        abstracts_similarity_matrix = (
            self.similarity_calculator.calculate_abstract_similarity(
                embedded_abstracts=embedded_abstracts
            )
        )
        progress_manager.update(task_id=cluster_publications_task_id, visible=False)
        progress_manager.print("[green]Clustered publications ✓")

        generate_dendogram_task_id = progress_manager.add_task(
            description="Generating dendogram... it will take a while", total=None
        )
        dendogram_labels = array(
            [
                processed_entry["title"]
                for processed_entry in processed_bibliography_entries
            ],
            dtype=str,
        )

        self.dendogram_builder.build_dendogram_and_save(
            similarity_matrix=abstracts_similarity_matrix,
            result_file=result_file,
            dendogram_labels=dendogram_labels,
        )
        progress_manager.update(task_id=generate_dendogram_task_id, visible=False)
        progress_manager.print("[green]Generated dendogram ✓")
