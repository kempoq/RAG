import logging
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import TextSplitter

logger = logging.getLogger(__name__)


class DocumentsService:
    def __init__(self, text_splitter: TextSplitter, dir: str) -> None:
        self._text_splitter = text_splitter
        self.dir = Path(dir)

    def get_filenames(self, ext: str) -> list[str]:
        """Возвращает список файлов указанного расширения в указанной директории"""

        return [file_path.name for file_path in self.dir.glob(f"*.{ext}")]

    def _get_documents(
        self, exclude_sources: list[str], ext: str
    ) -> tuple[list[str], list[Document]]:
        """Возвращает список файлов и документов (содержимое файлов, инкапсулированное в класс Document)"""

        logger.debug("Start collection documents")
        docs = []
        files = []

        for file_path in self.dir.glob(f"*.{ext}"):
            if file_path.is_file() and file_path.name not in exclude_sources:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
                    if len(content) == 0:
                        continue

                    files.append(file_path.name)
                    docs.append(
                        Document(
                            page_content=content,
                            metadata={"source": file_path.name},
                        )
                    )

        logger.debug("Documents are collected")
        return files, docs

    def get_documents_by_chunks(
        self, exclude_sources: list[str], ext: str = "txt"
    ) -> tuple[list[str], list[Document]]:
        """Возвращает список документов, разделенных на чанки"""

        files, docs = self._get_documents(exclude_sources, ext)
        if not docs:
            return files, docs

        logger.info("Start splitting documents")
        chunks = self._text_splitter.split_documents(docs)
        logger.info("Documents are splitted")

        return files, chunks
