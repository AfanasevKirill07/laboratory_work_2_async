"""Вспомогательные функции для замера времени.

    with print_time():      # печатает общее время блока
        main()

    log("alice: ответ")     # печатает строку с меткой времени от старта:
                            # [ 0.5s] alice: ответ
"""

from contextlib import contextmanager
from time import monotonic

_start = monotonic()


def log(message: str) -> None:
    print(f"[{monotonic() - _start:5.1f}s] {message}")


@contextmanager
def print_time():
    global _start
    _start = monotonic()
    yield
    print(f"Time elapsed: {monotonic() - _start:.2f}s")
