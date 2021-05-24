#!/usr/bin/env python3
import logging
import asyncio
import time


logging.getLogger().setLevel(logging.INFO)


async def count(num):
    logging.info(f"One {num}")
    await asyncio.sleep(1)
    logging.info(f"Two {num}")
    return num*num


async def main():
    tasks = []
    for i in range(3):
        task = asyncio.ensure_future(count(i+1))
        tasks.append(task)
    responses = await asyncio.gather(*tasks)
    logging.info("response of count function called multiple time")
    logging.info(f"{responses}")
    return responses

if __name__ == "__main__":
    s = time.perf_counter()
    res = asyncio.run(main())
    import pdb;
    pdb.set_trace()
    logging.info(res)
    elapsed_time = time.perf_counter() - s
    logging.info(f" executed in {elapsed_time:0.2f} seconds")



