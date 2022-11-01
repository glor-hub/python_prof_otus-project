import asyncio
import os
from dotenv import load_dotenv
from os.path import join, dirname, abspath

import logging

# from vksearch.vkgroup.vkapi_services.community import CommunityTask

load_dotenv()
TOKEN_NUM = 3

TOKEN = os.getenv('VK_API_TOKEN')
VERSION = os.getenv('VK_API_VERSION')


class VKApiClient:

    def __init__(self, period, session):
        self.session = session
        self.period = period
        self.token_list = self.get_token_list()
        self.queue = asyncio.Queue()
        self.tasks = []
        self.semaphore = asyncio.Semaphore(value=TOKEN_NUM)

    @staticmethod
    def get_token_list():
        list_token = []
        path = os.path.abspath(os.path.join(__file__, "../../.."))
        with open(join(path, 'tokens.txt')) as f:
            for line in f:
                list_token.append(str(line).rstrip('\n'))
        return list_token

    async def run(self):
        print(len(self.token_list))
        comm_task = CommunityTask()
        task1 = asyncio.create_task(comm_task.vk_get_communities(self.session, self.token_list[9]))
        self.tasks.append(task1)
        # task2 = asyncio.create_task(self.process_urls_forever())
        # self.tasks.append(task2)
        await asyncio.gather(*self.tasks)
        # print(list_token)
        # print(len(list_token))
