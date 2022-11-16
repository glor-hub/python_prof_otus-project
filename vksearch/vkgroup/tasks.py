from __future__ import absolute_import, unicode_literals

from django.db import IntegrityError

import logging
import time

import requests

from vksearch.celery import celery_app
from celery import group, shared_task

from datetime import datetime

from . import vkapiclient

from .models import Community, CommunityType, Country


def get_communities_data():
    min_id = 1
    vk_client = vkapiclient.VKApiClient()
    create_community_type()
    while True:
        url_list, min_id_next = vk_client.build_community_url_list(min_id)
        # print(url_list)
        # time.sleep(0)
        res = group(task_load_and_store_communities.s(url) for url in url_list)().get()
        for i in range(len(res)):
            if res[i] == 'Task completed':
                return
        min_id = min_id_next


@shared_task(
    default_retry_delay=1,
    autoretry_for=(Exception,),
    max_retries=3,
)
def task_load_and_store_communities(url):
    r = requests.get(url, timeout=(vkapiclient.REQ_CONNECT_TIMEOUT, vkapiclient.REQ_READ_TIMEOUT))
    data_list = r.json().get('response')

    if data_list:
        # logging.info(f'communities data from request number {count} received')
        # print(data_list)
        #
        for data in data_list:
            vk_id = data.get('id')
            if vk_id > vkapiclient.MAX_GROUPS_COUNT:
                return 'Task completed'
            dtype = data.get('type')
            CommunityType.objects.get_or_create(
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
                comm = Community.objects.create(
                    **params
                )
            except IntegrityError:
                comm = Community.objects.get(vk_id=vk_id)
                comm.deactivated = bool(data.get('deactivated'))
                comm.description = data.get('description')
                comm.verified = data.get('verified')
                comm.age_vk = data.get('age_limits')
                comm.name = data.get('name')
                comm.site = data.get('site')
                comm.members = data.get('members_count')
                comm.status = data.get('status')
                comm.is_updated = datetime.now()
                comm.save()
    # time.sleep(0.1)
    return 'Task in progress'


def get_countries_data():
    task_load_and_store_countries.delay()


@shared_task(
    default_retry_delay=1,
    autoretry_for=(Exception,),
    max_retries=3,
)
def task_load_and_store_countries():
    vk_client = vkapiclient.VKApiClient()
    url = vk_client.build_countries_url()
    r = requests.get(url, timeout=(vkapiclient.REQ_CONNECT_TIMEOUT, vkapiclient.REQ_READ_TIMEOUT))
    data_list = r.json().get('response')
    if data_list:
        # logging.info(f'communities data from request number {count} received')
        for data in data_list:
            id = data.get('id')
            params = {
                'pk': id,
                'name': data.get('title')
            }
            try:
                c= Country.objects.create(
                    **params
                )
            except IntegrityError:
                c = Country.objects.get(id=id)
                c.name = data.get('title')
                c.save()
        # time.sleep(0.2)
    return 'Task completed'


# def create_community_type():
#     task_create_community_type.delay()



def create_community_type():
    types = ['group', 'page', 'event']
    for type in types:
        comm_type, _ = CommunityType.objects.get_or_create(
            name=type,
        )
    return 'Task completed'
