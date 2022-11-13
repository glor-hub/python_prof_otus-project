from __future__ import absolute_import, unicode_literals

from django.db import IntegrityError

import logging
import time

import requests

from vksearch.celery import celery_app
from celery import group, shared_task

from datetime import datetime

from . import vkapiclient

from .models import Community, CommunityType


# token = vkapiclient.VKApiClient.get_token_list()[0]
# version = vkapiclient.VERSION
# ids = ','.join(str(id) for id in range(1, 12))

# URL_PATTERN = (
#     'https://api.vk.com/method/groups.getById?group_ids={ids}&'
#     'fields=type,is_closed,name,description,members_count,status,verified,site,age_limits&'
#     'v={version}&access_token={token}')


# def build_url(ids, version, token):
#     return URL_PATTERN.format(ids=ids, version=version, token=token)
#
#
# url = build_url(ids, version, token)


# URL_PATTERN = (
#         'https://api.vk.com/method/groups.getById?group_ids=1,2&'
#         'fields=type,is_closed,name,description,members_count,status,verified,site,age_limits&'
#         'v={version}&access_token={"vk1.a.vA6ydNiOLRpf3IDLi12zMHNauVVSkKsnvhf8vEuC2t4uk_avlq_l5MgPcIxxyQXMJq5jjXPjNSsZXYu0luY-tPutJe9UPRzFrt2Tz1Zglbq1ONLn1Twp_a7Z8WwFshqcpsVniscr7tyqmEBPW2EOq3kG8df5ktC667tUWJjSXBOHHSPRbvlKcaH3vfmepCrjhXpcWKU1qZGvYuUBZyu0Qw
# "}')

# @shared_task()
# def task_vk_get_data_communities(ids, version, token):
#     url = build_url(ids, version, token)
#     r = requests.get(url)
#     comm_data_list = r.json().get('response')
#     return comm_data_list

def vk_get_communities_data():
    min_id = 1
    offset = vkapiclient.MAX_GROUPS_COUNT_PER_REQUEST
    vk_client = vkapiclient.VKApiClient()
    pattern = vkapiclient.URL_PATTERN_GROUPS_BY_ID
    while True:
        url_list, min_id_next = vk_client.get_url_list(
            pattern=pattern,
            min_id=min_id,
            offset=offset
        )
        # print(url_list)
        res = group(task_vk_get_data.s(url) for url in url_list)().get()
        for i in range(len(res)):
            if res[i] == 'Task completed':
                return
        min_id = min_id_next


@shared_task(
    default_retry_delay=1,
    autoretry_for=(Exception,),
    max_retries=3,
)
def task_vk_get_data(url):
    r = requests.get(url, timeout=(vkapiclient.REQ_CONNECT_TIMEOUT, vkapiclient.REQ_READ_TIMEOUT))
    data_list = r.json().get('response')
    if data_list:
        # logging.info(f'communities data from request number {count} received')
        # print(data_list)
        types = ['group', 'page', 'event']
        for type in types:
            comm_type, _ = CommunityType.objects.get_or_create(
                name=type,
            )
        # print(comm_type)

        for data in data_list:
            vk_id = data.get('id')
            if vk_id > vkapiclient.MAX_GROUPS_COUNT:
                return 'Task completed'
            dtype = data.get('type')
            comm_type, _ = CommunityType.objects.get_or_create(
                name=dtype
            )
            params = {
                'vk_id': vk_id,
                'deactivated': bool(data.get('deactivated')),
                'description': data.get('description'),
                'verified': data.get('verified'),
                'age_vk': data.get('age_limits'),
                'name': data.get('name'),
                'site': data.get('site'),
                'members': data.get('members_count'),
                'status': data.get('status')
            }
            try:
                comm, created = Community.objects.get_or_create(
                    **params
                )
                if created:
                    comm.type = comm_type
                    comm.save()
            except IntegrityError:
                pass
        # time.sleep(0.2)
    return 'Task in progress'

# def vk_get_communities_data():
#     communities_count=vkapiclient.MAX_GROUPS_COUNT
#     min_id = 1
#     offset = vkapiclient.MAX_GROUPS_COUNT_PER_REQUEST
#     vk_client = vkapiclient.VKApiClient()
#     pattern = vkapiclient.URL_PATTERN_GROUPS_BY_ID
#     while True:
#         url_list, min_id_next = vk_client.get_url_list(
#             pattern=pattern,
#             min_id=min_id,
#             offset=offset
#         )
#         # print(url_list)
#         res = group(task_vk_get_data.s(url) for url in url_list)().get()
#         for i in range(len(res)):
#             if res[i] == 'Task completed':
#                 return
#         min_id = min_id_next
#

# @shared_task(
#     default_retry_delay=1,
#     autoretry_for=(Exception,),
#     max_retries=3,
# )
# def task_vk_get_user_profiles(url):
#     r = requests.get(url, timeout=(vkapiclient.REQ_CONNECT_TIMEOUT, vkapiclient.REQ_READ_TIMEOUT))
#     data_list = r.json().get('response')
#     if data_list:
#         # logging.info(f'communities data from request number {count} received')
#         # print(data_list)
#         types = ['group', 'page', 'event']
#         for type in types:
#             comm_type, _ = CommunityType.objects.get_or_create(
#                 name=type,
#             )
#         # print(comm_type)
#
#         for data in data_list:
#             dtype = data.get('type')
#             comm_type, _ = CommunityType.objects.get_or_create(
#                 name=dtype
#             )
#             params = {
#                 'vk_id': data.get('id'),
#                 'deactivated': bool(data.get('deactivated')),
#                 'description': data.get('description'),
#                 'verified': data.get('verified'),
#                 'age_vk': data.get('age_limits'),
#                 'name': data.get('name'),
#                 'site': data.get('site'),
#                 'members': data.get('members_count'),
#                 'status': data.get('status')
#             }
#             try:
#                 comm, created = Community.objects.get_or_create(
#                 **params
#             )
#                 if created:
#                     comm.type = comm_type
#                     comm.save()
#             except IntegrityError:
#                 pass
#         # time.sleep(0.2)
#         if len(data_list) < vkapiclient.MAX_GROUPS_COUNT_PER_REQUEST:
#             return 'Task completed'
#     return 'Task in progress'
