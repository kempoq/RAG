from app.src.core.database.vector_database import get_vector_store

if __name__ == "__main__":
    vs = get_vector_store()
    print(vs.get())
