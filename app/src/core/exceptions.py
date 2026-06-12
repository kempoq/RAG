class ApiError(Exception):
    """Общая ошибка API"""

    def __init__(self, type: str, msg: str, original_error: Exception) -> None:
        error_msg = f"{type}: {msg}\n[Details]: {original_error}"
        super().__init__(error_msg)


class VectoreDbError(ApiError):
    """Ошибка, связанная с векторной БД"""

    def __init__(self, msg: str, original_error: Exception) -> None:
        super().__init__("ChromaDB", msg, original_error)


class GraphDbError(ApiError):
    """Ошибка, связанная с графовой БД"""

    def __init__(self, msg: str, original_error: Exception) -> None:
        super().__init__("Neo4j", msg, original_error)


class WorkflowGenerationError(ApiError):
    """Ошибка при генерации графа операций для графового RAG"""

    def __init__(self, msg: str, original_error: Exception) -> None:
        super().__init__("GraphRAG", msg, original_error)
