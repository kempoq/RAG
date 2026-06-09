import logging

from fastapi import UploadFile
from langchain_core.documents import Document
from langchain_text_splitters import TextSplitter

logger = logging.getLogger(__name__)


class DocumentsService:
    def __init__(self, text_splitter: TextSplitter) -> None:
        self._text_splitter = text_splitter

    def _get_documents(
        self, files: list[UploadFile], exclude_sources: list[str]
    ) -> list[Document]:
        """Возвращает список документов (содержимое файлов, инкапсулированное в класс Document)"""

        logger.debug("Start collection documents")
        docs = []

        for file in files:
            if file.filename in exclude_sources or file.size == 0:
                continue

            docs.append(
                Document(
                    page_content=file.file.read().decode("utf-8"),
                    metadata={"source": file.filename},
                )
            )

        logger.debug("Documents are collected")
        return docs

    def get_document_chunks(
        self, files: list[UploadFile], exclude_sources: list[str]
    ) -> list[Document]:
        """Возвращает список документов, разделенных на чанки"""

        docs = self._get_documents(files, exclude_sources)
        if not docs:
            return docs

        logger.info("Start splitting documents")
        chunks = self._text_splitter.split_documents(docs)
        logger.info("Documents are splitted")

        return chunks
