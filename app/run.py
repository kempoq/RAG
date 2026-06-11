import uvicorn


def main() -> None:
    uvicorn.run(
        "app.src.main:app", host="127.0.0.1", port=8000, log_config=None, reload=True
    )


if __name__ == "__main__":
    main()
