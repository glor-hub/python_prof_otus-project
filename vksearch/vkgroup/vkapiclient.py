import asyncio
import os
from dotenv import load_dotenv
from os.path import join, dirname, abspath

import logging

# from vksearch.vkgroup.vkapi_services.community import CommunityTask

load_dotenv()
# TOKEN_NUM = 3

# TOKEN = os.getenv('VK_API_TOKEN')
VERSION = os.getenv('VK_API_VERSION')
UPDATE_DATA_PERIOD = os.getenv('VK_UPDATE_DATA_PERIOD')
MIN_TIME_PER_REQUEST = os.getenv('VK_MIN_TIME_PER_REQUEST')
MAX_GROUPS_COUNT_PER_REQUEST = 500
REQ_CONNECT_TIMEOUT = 1
REQ_READ_TIMEOUT = 3
MAX_GROUPS_COUNT=100000

URL_PATTERN_GROUPS_BY_ID = (
    'https://api.vk.com/method/groups.getById?group_ids={ids}&'
    'fields=type,is_closed,name,description,members_count,status,verified,site,age_limits&'
    'v={version}&access_token={token}')


class VKApiClient:

    def __init__(self):
        self.version = VERSION
        self.update_period = UPDATE_DATA_PERIOD
        self.min_req_time = MIN_TIME_PER_REQUEST
        self.token_list = self.get_token_list()
        # self.tokens_count=len(self.token_list)
        # self.queue = asyncio.Queue()
        # self.tasks = []
        # self.semaphore = asyncio.Semaphore(value=TOKEN_NUM)

    def get_token_list(self):
        token_list = []
        path = os.path.abspath(os.path.join(__file__, "../../"))
        with open(join(path, 'tokens.txt')) as f:
            for line in f:
                token_list.append(str(line).rstrip('\n'))
        self.token_list = token_list
        return token_list

    def get_url_list(self, pattern, min_id, offset):
        url_list = []
        for token in self.token_list:
            ids = ','.join(str(id) for id in range(int(min_id), int(min_id + offset)))
            url_list.append(pattern.format(ids=ids, version=self.version, token=token))
            min_id += offset
        return url_list, min_id

    # async def run(self):
    #     print(len(self.token_list))
    #     comm_task = CommunityTask()
    #     task1 = asyncio.create_task(comm_task.vk_get_communities(self.session, self.token_list[9]))
    #     self.tasks.append(task1)
    #     # task2 = asyncio.create_task(self.process_urls_forever())
    #     # self.tasks.append(task2)
    #     await asyncio.gather(*self.tasks)
    #     # print(token_list)
    #     # print(len(list_token))
