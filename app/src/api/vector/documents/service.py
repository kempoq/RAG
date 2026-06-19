import logging

from fastapi import UploadFile
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


class DocumentsService:
    def __init__(self, text_splitter: RecursiveCharacterTextSplitter) -> None:
        self._text_splitter = text_splitter

    def get_documents_splitted_by_chunks(
        self, files: list[UploadFile], exclude_sources: list[str]
    ) -> list[Document]:
        """Возвращает список документов (содержимое файлов, разбитое по чанкам, инкапсулированное в класс Document)"""

        logger.info("Start splitting files' content")
        docs = []

        for file in files:
            if file.filename in exclude_sources or file.size == 0:
                continue
            logger.info(f"Splitting text in file {file.filename}")

            chunks = self._text_splitter.split_text(file.file.read().decode("utf-8"))

            logger.debug(f"Chunks count - {len(chunks)}")
            for chunk in chunks:
                docs.append(
                    Document(page_content=chunk, metadata={"source": file.filename})
                )

        logger.info("Files are splitted and wraped into documents")
        return docs
