"""Шаг 4 (дополнительный). Блокировка event loop.

Ниже готовый асинхронный сервер из шага 3б. Но теперь клиент "bob"
прислал не запрос в базу, а задачу на тяжёлые вычисления: функция
heavy_compute. Она синхронная и работает 1-3 секунды в зависимости от машины.

Задание 4а:
  В handle_request для клиента "bob" вызовите heavy_compute()
  вместо await asyncio.sleep(duration). Остальные клиенты по-прежнему
  ждут через asyncio.sleep. Запустите.
  Что произошло с остальными клиентами? Почему, ведь всё написано на async?

Задание 4б:
  Исправьте так, чтобы остальные клиенты не ждали bob. Два инструмента:
    await asyncio.to_thread(heavy_compute)
    await loop.run_in_executor(pool, heavy_compute)
  где loop = asyncio.get_running_loop(), а pool — это ProcessPoolExecutor
  из concurrent.futures, открытый через with в main.
  Попробуйте оба. Порядок строк в выводе должен стать как в шаге 3б,
  время bob зависит от машины.

Задание 4в (если осталось время):
  Сделайте тяжёлыми трёх клиентов: bob, dave и eve. Сравните общее время
  для to_thread и для пула процессов. Почему оно отличается? Вспомните GIL.
"""

import asyncio
import concurrent.futures

from timer import log, print_time

CLIENTS = [
    ("alice", 0.5),
    ("bob", 5.0),
    ("carol", 0.5),
    ("dave", 0.5),
    ("eve", 0.5),
]


def heavy_compute() -> int:
    """Синхронные тяжёлые вычисления, 1-3 секунды."""
    h = 0
    for i in range(30_000_000):
        h = (h * 31 + i) & 0xFFFFFFFF
    return h


async def handle_request_thread(client: str, duration: float) -> None:
    """Вариант 4б: использование asyncio.to_thread"""
    log(f"{client}: запрос принят")
    if client == "bob":
        await asyncio.to_thread(heavy_compute)
    else:
        await asyncio.sleep(duration)
    log(f"{client}: ответ отправлен")


async def handle_request_process(client: str, duration: float, pool: concurrent.futures.ProcessPoolExecutor) -> None:
    """Вариант 4б: использование ProcessPoolExecutor"""
    log(f"{client}: запрос принят")
    loop = asyncio.get_running_loop()
    if client == "bob":
        await loop.run_in_executor(pool, heavy_compute)
    else:
        await asyncio.sleep(duration)
    log(f"{client}: ответ отправлен")


async def main_thread() -> None:
    """Запуск с использованием потоков (to_thread)"""
    coroutines = [handle_request_thread(client, duration) for client, duration in CLIENTS]
    await asyncio.gather(*coroutines)


async def main_process() -> None:
    """Запуск с использованием процессов (ProcessPoolExecutor)"""
    with concurrent.futures.ProcessPoolExecutor() as pool:
        coroutines = [handle_request_process(client, duration, pool) for client, duration in CLIENTS]
        await asyncio.gather(*coroutines)


if __name__ == "__main__":
    print("--- 4б: Вариант с asyncio.to_thread ---")
    with print_time():
        asyncio.run(main_thread())

    print("\n--- 4б: Вариант с ProcessPoolExecutor ---")
    with print_time():
        asyncio.run(main_process())
