import asyncio
import logging

import aiohttp

from .vkapiclient import VKApiClient


def logging_init(logging_file):
    # initialize script logging
    logging.basicConfig(filename=logging_file,
                        format='[%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)


async def main():
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10)
    ) as session:
        vkclient = VKApiClient(2, session)
        await vkclient.run()


# if __name__ == '__main__':
#     logging_init(None)
#
#     asyncio.run(main())

def main_run():
    logging_init(None)

    asyncio.run(main())
