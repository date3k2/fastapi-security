import aiohttp
import time
import httpx
import asyncio
from datetime import datetime
from itertools import product
from random import uniform

# Định nghĩa hàm async để gửi yêu cầu
username = "bxkozw"

url = "http://127.0.0.1:8000/login"


async def send_request_async(client: httpx.AsyncClient, password):
    response = await client.post(
        url,
        json={"username": username, "password": password},
    )
    # print(password, response.status_code, "at", datetime.now())


async def send(session: aiohttp.ClientSession, password):
    resp = await session.request(
        "POST", url, json={"username": username, "password": password}
    )
    # print(password, resp.status)


# Sử dụng asyncio để chạy các coroutine đồng thời
async def main():
    tasks = []
    # send 10 requests at a time
    async with aiohttp.ClientSession() as client:
        for i, x in enumerate(product("0123456789", repeat=2)):
            password = "".join(x)
            tasks.append(send(client, password))
            if (i + 1) % 5 == 0:
                await asyncio.gather(*tasks, return_exceptions=True)
                tasks = []
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)


# Chạy event loop

# start = time.time()
# asyncio.run(main())
# print("Time:", time.time() - start)


# httpx.AsyncClient() as client:
import timeit
if __name__ == "__main__":
    print(
        timeit.timeit(
            "asyncio.run(main())",
            setup="from __main__ import main, asyncio",
            number=10,
        )
    )
