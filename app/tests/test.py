from app.src.core.ml_models import get_llm

if __name__ == "__main__":
    giga = get_llm()

    ai_message = giga.invoke(
        "Напиши Cypher: MATCH (n) RETURN count(n). Выведи только запрос"
    )
