from langchain_core.messages import AIMessage, HumanMessage

from app.src.api.graph.utlis import extract_response_data

if __name__ == "__main__":
    arr = [
        HumanMessage(content="dasdsa", response_metadata={"a": 1, "d": 5}),
        AIMessage(content="dasdsa", response_metadata={"das": 1, "dasd": 4}),
    ]
    state = {
        "question": "question",
        "answer": "answer",
        "database_context": {"cypher_query": "123", "raw_results": [{"a": 1, "b": 2}]},
        "message_history": arr,
    }

    print(extract_response_data(state))
