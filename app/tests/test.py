import numpy as np

from app.src.api.graph.utils import merge_dicts_one_deep
from app.src.core.ml_models import get_embedding_model_api


def test_embeddings():
    emb_model = get_embedding_model_api()

    test_texts = [
        "a",
        "The quick brown fox jumps over the lazy dog.",
        "Quantum computing leverages superposition and entanglement.",
        "12345",
        "",
    ]

    print("L2 norm checks:")
    for text in test_texts:
        vec = emb_model.embed_query(text)
        norm = np.linalg.norm(vec)
        dim = len(vec)
        print(f"  '{text[:30]:<30}' → norm={norm:.6f}, dim={dim}")

    batch = emb_model.embed_documents(test_texts)
    print(f"\nBatch norms: {[np.linalg.norm(v) for v in batch]}")


if __name__ == "__main__":
    d1 = {"first": {"one": 1, "two": 2}, "second": [1, 2, 3], "third": 5}
    d2 = {"first": {"three": 3, "four": 4}, "second": [4, 5, 6]}
    print(merge_dicts_one_deep(d1, d2))
