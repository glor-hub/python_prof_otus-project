import logging

from . import vkapiclient
from .base_task import BaseTask
from ..models import Community

logger = logging.getLogger(__name__)


class CommunityTask(BaseTask):
    IDS_PER_TASK = 8
    URL_PATTERN = (
        'https://api.vk.com/method/groups.getById?group_ids={ids}&'
        'fields=type,is_closed,name,description,members_count,status,verified,site,age_limits&'
        'v={version}&access_token={token}')

    def __init__(self):
        self.response = None
        self.comm_load_is_finished = None

    def build_url(self, ids, version, token):
        return self.URL_PATTERN.format(ids=ids, version=version, token=token)

    async def vk_get_communities(self, session, token):
        ids = ','.join(str(id) for id in range(1, self.IDS_PER_TASK))
        print(ids)
        version = vkapiclient.VERSION
        url = self.build_url(ids, version, token)
        # print(url)
        self.response = await super().get_data(session, url)
        self.handle_response(self.response)

    def handle_error(self):
        errmsg = 'Unknown  error occurred'
        err = self.response.get('error')
        if err:
            errmsg = err.get('error_msg', errmsg)
            logging.error(errmsg)
            raise Exception

    def handle_response(self, resp):
        count = 0
        data_list = resp.get('response')
        # print('type',type(data_list[0]))
        if data_list:
            logging.info(f'data received')
            print(data_list)
            for data in data_list:
                # count += 1
                # if data.get('deactivated') or not data.get('members'):
                #     continue
                vk_id = int(data.get('id'))
                print(vk_id)
                comm=Community.objects.get_or_create(
                    vk_id=vk_id)
                print(comm)
                #     deactivated=False)
            # if count!=self.IDS_PER_TASK:
            #     self.comm_load_is_finished = True

                # parse_and_save_to_db(data)
        else:
            self.handle_error()
