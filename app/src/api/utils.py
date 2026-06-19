from fastapi import Response


def set_cache_control_headers(response: Response) -> None:
    """Устанавливает Cache Control заголовки в HTTP овтет (response)"""

    response.headers["Cache-Control"] = "private, max-age=300, must-revalidate"
