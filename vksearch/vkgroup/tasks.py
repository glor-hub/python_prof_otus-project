from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

import logging
import time

import requests

from vksearch.celery import celery_app
from celery import group, shared_task

from datetime import datetime

from . import vkapiclient

from .models import Community, CommunityType, Country, AudienceProfile, Audience, AgeRange


# def get_communities_data(update_flag=False):
#     min_id = 1
#     vk_client = vkapiclient.VKApiClient()
#     create_community_types()
#     while True:
#         url_list, min_id_next = vk_client.build_community_url_list(min_id)
#         # print(url_list)
#         # time.sleep(0)
#         if update_flag:
#             res = group(task_update_and_store_communities.s(url) for url in url_list)().get()
#         else:
#             res = group(task_load_and_store_communities.s(url) for url in url_list)().get()
#         for i in range(len(res)):
#             if res[i] == 'Task completed':
#                 return
#         min_id = min_id_next

def get_communities_data(update_flag=False):
    min_id = 1
    vk_client = vkapiclient.VKApiClient()
    CommunityType.create_table_with_data()
    while True:
        url_list, min_id_next = vk_client.build_community_url_list(min_id)
        # print(url_list)
        # time.sleep(0)
        if update_flag:
            res = group(task_update_and_store_communities.s(url) for url in url_list).apply_async().get()
        else:
            res = group(task_load_and_store_communities.s(url) for url in url_list).apply_async().get()
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
            c_type, _ = CommunityType.objects.get_or_create(
                name=dtype
            )
            params = {
                'vk_id': vk_id,
                'type': c_type,
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
                    comm.type = c_type
                    comm.save()
            except IntegrityError:
                pass
    # time.sleep(0.1)
    return 'Task in progress'


@shared_task(
    default_retry_delay=1,
    autoretry_for=(Exception,),
    max_retries=3,
)
def task_update_and_store_communities(url):
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
            c_type, _ = CommunityType.objects.get_or_create(
                name=dtype
            )
            comm = Community.objects.get(vk_id=vk_id)
            comm.type = c_type
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
                c, _ = Country.objects.get_or_create(
                    **params
                )
            except IntegrityError:
                c = Country.objects.get(id=id)
                c.name = data.get('title')
                c.save()
        # time.sleep(0.2)
    return 'Task completed'


# def create_community_types():
#     types = ['group', 'page', 'event']
#     for type in types:
#         comm_type, _ = CommunityType.objects.get_or_create(
#             name=type,
#         )
#     return 'Task completed'


def check_for_update_data_from_vk():
    try:
        comm = Community.objects.get(vk_id=1)
        if (datetime.now() - comm.is_updated).total_seconds() > float(vkapiclient.UPDATE_DATA_PERIOD):
            get_communities_data(update_flag=True)
    except ObjectDoesNotExist:
        get_communities_data(update_flag=False)
        get_countries_data()
        AgeRange.create_table_with_data()
        # create_audience_profile()
    process_audience()


def process_audience():
    get_audience_data()


def get_audience_data():
    comms = Community.objects.filter(deactivated=False).order_by('vk_id')
    for comm in comms:
        vk_id=comm.vk_id
        get_audience_data_for_group(vk_id)


def get_audience_data_for_group(g_id):
    vk_client = vkapiclient.VKApiClient()
    url_list = vk_client.build_audience_url_list(g_id)
    res = group([task_load_users_for_community.s(url, g_id) for url in url_list]).apply_async().get()
    for i in range(len(res)):
        if res[i] == 'Task completed':
            return


@shared_task(
    default_retry_delay=1,
    autoretry_for=(Exception,),
    max_retries=3,
)
def task_load_users_for_community(url, g_id):
    vk_client = vkapiclient.VKApiClient()
    r = requests.get(url, timeout=(vkapiclient.REQ_CONNECT_TIMEOUT, vkapiclient.REQ_READ_TIMEOUT))
    data_list = r.json().get('response').get('items')
    if data_list:
        # logging.info(f'communities data from request number {count} received')
        for data in data_list:
            if not data:
                continue
            age_range = vk_client.parse_bdate(data.get('bdate'))
            country = vk_client.parse_country(data.get('country'))
            sex = vk_client.parse_sex(data.get('sex'))
            params = {
                'age_range': age_range,
                'country': country,
                'sex': sex
            }
            aud_profile, created = AudienceProfile.objects.get_or_create(
                **params
            )
            comm_aud, created = Audience.objects.get_or_create(
                community__vk_id=g_id,
                profile=aud_profile
            )
            comm_aud.count += 1
            comm_aud.save()
            # print(comm_aud)
        # time.sleep(0.2)
    return 'Task completed'
