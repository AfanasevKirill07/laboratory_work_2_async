"""Шаг 1. Синхронная программа.

Задание: реализуйте функцию work(n), которая
  1. печатает "start n"
  2. ждёт 1 секунду (time.sleep)
  3. печатает "done n"

и функцию main(), которая вызывает work для n от 1 до 10.
Запустите с замером времени. Сколько секунд заняла программа?
"""

import time

from timer import print_time


def work(n: int) -> None:
    ...


def main() -> None:
    ...


if __name__ == "__main__":
    with print_time():
        main()
