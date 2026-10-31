"""Шаг 2. Переписываем на asyncio.

Задание 2а:
  1. Сделайте work корутиной (async def).
  2. Замените time.sleep на await asyncio.sleep.
  3. Сделайте main корутиной и вызовите в ней work через await в цикле.
  4. Запустите через asyncio.run.

Замерьте время. Изменилось ли оно по сравнению с шагом 1? Почему?

Задание 2б:
  Перепишите main так, чтобы все 10 задач ждали одновременно.
  Подсказка: asyncio.gather. Что изменилось в порядке вывода?
"""

import asyncio

from timer import print_time


async def work(n: int) -> None:
    print(f"start {n}")
    await asyncio.sleep(1)
    print(f"done {n}")


async def main_sequential() -> None:
    # 2а: последовательный вызов
    for n in range(1, 11):
        await work(n)


async def main_concurrent() -> None:
    # 2б: конкурентный вызов
    coroutines = [work(n) for n in range(1, 11)]
    await asyncio.gather(*coroutines)


if __name__ == "__main__":
    # Сначала запустим 2а (последовательно), потом 2б (конкурентно)
    print("--- 2а: последовательный запуск (ожидаемое время ~10.00s) ---")
    with print_time():
        asyncio.run(main_sequential())

    print("\n--- 2б: конкурентный запуск (ожидаемое время ~1.00s) ---")
    with print_time():
        asyncio.run(main_concurrent())
