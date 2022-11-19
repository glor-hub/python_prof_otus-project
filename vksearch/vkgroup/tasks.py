from __future__ import absolute_import, unicode_literals

import os
from os.path import join

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

import logging
import time

import requests
from django.db.models import Q, F

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
    c = Country(id=238, name=Country.UNKNOWN_COUNTRY)
    c.save()
    # time.sleep(0.2)
    return 'Task completed'

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
    comms = Community.objects.filter(deactivated=False).exclude(Q(members__isnull=True) | Q(members__exact=0)).order_by(
        'vk_id')
    for comm in comms:
        vk_id = comm.vk_id
        if 2 <= vk_id <= 6:
            get_audience_data_for_group(vk_id)
    # get_audience_data_for_group(78)


def get_audience_data_for_group(g_id):
    vk_client = vkapiclient.VKApiClient()
    users_offset = 0
    # count=0
    while True:
        url_list = vk_client.build_audience_url_list(g_id, users_offset)
        if not url_list:
            return
        res = group(task_load_users_for_community.s(url, g_id) for url in url_list).apply_async().get()
        for i in range(len(res)):
            if res[i] == 'Task completed':
                return
        users_offset += len(vk_client.token_list) * vk_client.step * vk_client.max_requests


# res = group(task_update_and_store_communities.s(url) for url in url_list).apply_async().get()

@shared_task(
    default_retry_delay=1,
    autoretry_for=(Exception,),
    max_retries=3,
)
def task_load_users_for_community(url, g_id):
    vk_client = vkapiclient.VKApiClient()
    r = requests.get(url, timeout=(vkapiclient.REQ_CONNECT_TIMEOUT, vkapiclient.REQ_READ_TIMEOUT))
    response = r.json().get('response')
    # logging.info(f'communities data from request number {count} received')
    for resp in response:
        if not resp:
            continue
        data_list = resp.get('items')
        if not data_list:
            return 'Task completed'
        for data in data_list:
            country = vk_client.parse_country(data)
            age = AgeRange.objects.get(range=vk_client.parse_bdate(data))
            country = Country.objects.get(name=country)
            params = {
                "age_range": age,
                "sex": vk_client.parse_sex(data),
                "country": country
            }
            try:
                profile, _ = AudienceProfile.objects.get_or_create(
                    **params
                )
            except IntegrityError:
                profile, _ = AudienceProfile.objects.get(
                    **params
                )
            params = {
                "community": Community(vk_id=g_id),
                "profile": profile
            }
            audience, _ = Audience.objects.get_or_create(
                **params
            )
            audience.count = F('count') + 1
            audience.save(update_fields=["count"])

    time.sleep(5)
    return 'Task in progress'
  