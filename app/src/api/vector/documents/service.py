from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import TextSplitter


class DocumentsService:
    def __init__(self, text_splitter: TextSplitter, dir: str) -> None:
        self._text_splitter = text_splitter
        self.dir = Path(dir)

    def get_filenames(self, ext: str) -> list[str]:
        """Возвращает список файлов указанного расширения в указанной директории"""

        return [file_path.name for file_path in self.dir.glob(f"*.{ext}")]

    def _get_documents(self, ext: str) -> tuple[list[str], list[Document]]:
        """Возвращает список файлов и документов (содержимое файлов, инкапсулированное в класс Document)"""

        print("Start collection documents")
        docs = []
        files = []

        for file_path in self.dir.glob(f"*.{ext}"):
            if file_path.is_file():
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
                    if len(content) == 0:
                        continue

                    files.append(file_path.name)
                    docs.append(
                        Document(
                            page_content=content,
                            metadata={"source": file_path.name.split(".", 1)[0]},
                        )
                    )

        print("Documents are collected")
        return files, docs

    def get_documents_by_chunks(
        self, ext: str = "txt"
    ) -> tuple[list[str], list[Document]]:
        """Возвращает список документов, разделенных на чанки"""

        files, docs = self._get_documents(ext)
        if not docs:
            return files, docs

        print("Start splitting documents")
        chunks = self._text_splitter.split_documents(docs)
        print("Documents are splitted")

        return files, chunks
