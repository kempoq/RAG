import re


def extract_cypher_from_markdown(text: str) -> str:
    """Извлекает Cypher запрос из MarkDown блока Cypher кода (```cypher ... ```)"""

    pattern = r"```(?:[a-zA-Z]*\n)?(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return matches[0].strip()

    return text.strip()
