import logging
from typing import Any

import yaml

from app.src.core.config import settings


def parse_yaml_file(file_path: str) -> dict[Any, Any]:
    """Парсит YAML файлы в Python словари"""

    with open(file_path, mode="r") as f:
        return yaml.safe_load(f)


def configure_logging() -> None:
    """Применяет конфигурацию логирования из файла"""

    logging_conf = parse_yaml_file(settings.logging_conf_path)
    logging.config.dictConfig(logging_conf)
