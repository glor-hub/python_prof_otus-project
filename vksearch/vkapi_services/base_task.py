import logging
import asyncio

class BaseTask:
    MAX_RECONNECT_TRIES = 7
    INTERVAL_RETRIES = 1
    SUCCESS_STATUS = 200

    async def get_data(self,session,url):
        tries = 0
        while True:
            try:
                async with session.get(url) as resp:
                    if resp.status != self.SUCCESS_STATUS:
                        logging.info(f'status ={resp.status}, url: {url}')
                        await asyncio.sleep(self.INTERVAL_RETRIES * 2 ** tries)
                        tries += 1
                        # return None
                    else:
                        return await resp.read()
            except Exception:
                await asyncio.sleep(self.INTERVAL_RETRIES * 2 ** tries)
                tries += 1
            if tries > self.MAX_RECONNECT_TRIES:
                logging.error(f'Unable to load data')
                return None
