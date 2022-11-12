from __future__ import absolute_import, unicode_literals
import requests
from celery import shared_task
from datetime import datetime

from . import vkapiclient
from .models import Community, CommunityType

token = vkapiclient.VKApiClient.get_token_list()[0]
version = vkapiclient.VERSION
ids = ','.join(str(id) for id in range(1, 12))

URL_PATTERN = (
    'https://api.vk.com/method/groups.getById?group_ids={ids}&'
    'fields=type,is_closed,name,description,members_count,status,verified,site,age_limits&'
    'v={version}&access_token={token}')


def build_url(ids, version, token):
    return URL_PATTERN.format(ids=ids, version=version, token=token)


url = build_url(ids, version, token)


# URL_PATTERN = (
#         'https://api.vk.com/method/groups.getById?group_ids=1,2&'
#         'fields=type,is_closed,name,description,members_count,status,verified,site,age_limits&'
#         'v={version}&access_token={"vk1.a.vA6ydNiOLRpf3IDLi12zMHNauVVSkKsnvhf8vEuC2t4uk_avlq_l5MgPcIxxyQXMJq5jjXPjNSsZXYu0luY-tPutJe9UPRzFrt2Tz1Zglbq1ONLn1Twp_a7Z8WwFshqcpsVniscr7tyqmEBPW2EOq3kG8df5ktC667tUWJjSXBOHHSPRbvlKcaH3vfmepCrjhXpcWKU1qZGvYuUBZyu0Qw
# "}')

@shared_task()
def task_vk_get_data_communities(ids, version, token):
    url = build_url(ids, version, token)
    r = requests.get(url)
    comm_data_list = r.json().get('response')
    return comm_data_list


def parse_data_communities():
    pass


@shared_task()
def task_write_data_communities_to_db():
    pass


def process_data_communities():
    pass


@shared_task()
def test_create_task():
    r = requests.get(url)
    data_list = r.json().get('response')
    # print('type',type(data_list[0]))
    if data_list:
        # logging.info(f'data received')
        print(data_list)
        types = ['group', 'page', 'event']
        for type in types:
            comm_type,_ = CommunityType.objects.get_or_create(
                name=type,
            )
            print(comm_type)
        for data in data_list:
            # count += 1
            # if data.get('deactivated') or not data.get('members'):
            #     continue
            dtype = data.get('type')

            comm_type,_ = CommunityType.objects.get_or_create(
                name=dtype
            )
            params = {
                'vk_id': data.get('id'),
                'deactivated': bool(data.get('deactivated')),
                'description': data.get('description'),
                'verified': data.get('verified'),
                'age_vk': data.get('age_limits'),
                'name': data.get('name'),
                'site': data.get('site'),
                'members': data.get('members_count'),
                'status': data.get('status')
            }
            # vk_id = int(data.get('id'))
            # deactivated = int(data.get('deactivated'))
            # description = data.get('description')
            #
            # print(vk_id)

            comm,created = Community.objects.get_or_create(
                **params
                # vk_id=vk_id,
                # # deactivated=deactivated,
                # description=description
                # # verified=verified
            )
            # comm = Community.objects.get(
            #     vk_id=vk_id
            # )
            if created:
                comm.type = comm_type
                comm.save()
            print(comm)
        # print(r)
        return {"status": True}


print(token)
print(version)

print(URL_PATTERN)
print(ids)
