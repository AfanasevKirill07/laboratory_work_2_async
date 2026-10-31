"""Шаг 3. Эмуляция сервера (асинхронный вариант).

Задание 3б (асинхронный сервер):
  Скопируйте файл в step3_server_async.py и перепишите на asyncio так,
  чтобы запросы обрабатывались конкурентно.
  На какой секунде теперь получает ответ "carol"? А "bob"?
"""

import asyncio

from timer import log, print_time

# (клиент, сколько секунд база отвечает на его запрос)
CLIENTS = [
    ("alice", 0.5),
    ("bob", 5.0),
    ("carol", 0.5),
    ("dave", 0.5),
    ("eve", 0.5),
]


async def handle_request(client: str, duration: float) -> None:
    log(f"{client}: запрос принят")
    await asyncio.sleep(duration)
    log(f"{client}: ответ отправлен")


async def main() -> None:
    coroutines = [handle_request(client, duration) for client, duration in CLIENTS]
    await asyncio.gather(*coroutines)


if __name__ == "__main__":
    with print_time():
        asyncio.run(main())
