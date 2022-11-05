# -*- coding: utf-8 -*-
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
def create_task():
    r = requests.get(url)
    data_list = r.json().get('response')
    # print('type',type(data_list[0]))
    if data_list:
        # logging.info(f'data received')
        print(data_list)
        types = ['group', 'page', 'event']
        for type in types:
            comm_type = CommunityType.objects.get_or_create(
                name=type,
            )
            print(comm_type)
        for data in data_list:
            # count += 1
            # if data.get('deactivated') or not data.get('members'):
            #     continue
            vk_id = int(data.get('id'))
            type = data.get('type')
            # deactivated = int(data.get('deactivated'))
            description = data.get('description')
            # verified = int(data.get('verified'))
            print(vk_id)
            comm_type = CommunityType.objects.get(
                name=type
            )
            comm = Community.objects.get_or_create(
                vk_id=vk_id,
                # deactivated=deactivated,
                description=description
                # verified=verified
            )
            comm = Community.objects.get(
                vk_id=vk_id
                      )
            comm.type = comm_type

            comm.save()
            print(comm)
        # print(r)
        return {"status": True}


print(token)
print(version)

print(URL_PATTERN)
print(ids)
