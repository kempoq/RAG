from app.src.core.logger import configure_logging

if __name__ == "__main__":
    lo = configure_logging()
    print(type(lo))
