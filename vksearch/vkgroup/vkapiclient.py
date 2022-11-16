import asyncio
import os
from dotenv import load_dotenv
from os.path import join, dirname, abspath

import logging

# from vksearch.vkgroup.vkapi_services.community import CommunityTask
from .models import Community

load_dotenv()

VERSION = os.getenv('VK_API_VERSION')
UPDATE_DATA_PERIOD = os.getenv('VK_UPDATE_DATA_PERIOD')
MIN_TIME_PER_REQUEST = os.getenv('VK_MIN_TIME_PER_REQUEST')
REQ_CONNECT_TIMEOUT = 1
REQ_READ_TIMEOUT = 3
MAX_REQUESTS_PER_EXECUTE_METHOD = 25

# communities
MAX_GROUPS_COUNT_PER_REQUEST = 500
MAX_GROUPS_COUNT = 100000

URL_PATTERN_GROUPS_BY_ID = (
    'https://api.vk.com/method/groups.getById?group_ids={ids}&'
    'fields=type,is_closed,name,description,members_count,status,verified,site,age_limits&'
    'v={version}&access_token={token}')

# audience
MAX_GROUPS_MEMBERS_COUNT_PER_REQUEST = 5

URL_PATTERN_GROUPS_MEMBERS = (
    'https://api.vk.com/method/execute?code={code}&v={version}&access_token={token}'
)

CODE = ('API.groups.getMembers({"group_id":{id},"offset":{offset},"count":{count},"sort":"id_asc",'
        '"fields":"sex,bdate,country,city,last_seen"})')

# countries
MAX_COUNTRIES_COUNT = 237

URL_PATTERN_COUNTRIES_BY_ID = (
    'https://api.vk.com/method/database.getCountriesById?country_ids={ids}&'
    'v={version}&access_token={token}')


class VKApiClient:

    def __init__(self):
        self.version = VERSION
        self.update_period = UPDATE_DATA_PERIOD
        self.min_req_time = MIN_TIME_PER_REQUEST
        self.token_list = self.get_token_list()
        self.max_users_per_req = MAX_GROUPS_MEMBERS_COUNT_PER_REQUEST
        self.max_reqs_per_execute = MAX_REQUESTS_PER_EXECUTE_METHOD
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

    def build_community_url_list(self, min_id):
        url_list = []
        pattern = URL_PATTERN_GROUPS_BY_ID
        offset = MAX_GROUPS_COUNT_PER_REQUEST
        for token in self.token_list:
            ids = ','.join(str(id) for id in range(int(min_id), int(min_id + offset)))
            url_list.append(pattern.format(ids=ids, version=self.version, token=token))
            min_id += offset
        return url_list, min_id

    def build_countries_url(self):
        pattern = URL_PATTERN_COUNTRIES_BY_ID
        ids = ','.join(str(id) for id in range(1, MAX_COUNTRIES_COUNT + 1))
        token = self.token_list[0]
        url = pattern.format(ids=ids, version=self.version, token=token)
        return url

    def build_audience_url_list(self, group_id):
        url_list = []
        pattern = URL_PATTERN_GROUPS_MEMBERS
        comm = Community.objects.get(vk_id=group_id)
        group_members = comm.members
        if not group_members:
            return None
        # groups = Community.objects.filter(deactivated=False).order_by('pk')
        req_min = 0
        users = group_members
        for token in self.token_list:
            code, req = self.build_audience_url_code(group_id=group_id, users=users, req_min_num=req_min)

            url_list.append(pattern.format(code=code, version=self.version, token=token))
            if not req:
                return url_list
            req_min = req
            users -= self.max_users_per_req * self.max_reqs_per_execute

    def build_audience_url_code(self, group_id, users, req_min_num):
        reqs_count = users % self.max_users_per_req + 1
        users_count = MAX_GROUPS_MEMBERS_COUNT_PER_REQUEST
        if reqs_count <= self.max_reqs_per_execute:
            code = ','.join(
                CODE.format(id=group_id, offset=self.max_users_per_req * req_num, count=users_count) for req_num in
                range(req_min_num, reqs_count))
            req_min_next = 0
        else:
            code = ','.join(
                CODE.format(id=group_id, offset=self.max_users_per_req * req_num, count=users_count) for req_num in
                range(req_min_num, self.max_reqs_per_execute + 1))
            req_min_next = reqs_count + 1
        return (code, req_min_next)

    def parse_bdate(bdate):
        return bdate

    def parse_country(country):
        return country

    def parse_sex(sex):
        return sex
