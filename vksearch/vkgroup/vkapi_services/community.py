from . import vkapiclient
from .base_task import BaseTask

import logging
logger = logging.getLogger(__name__)

class CommunityTask(BaseTask):
    IDS_PER_TASK = 5
    URL_PATTERN = (
        'https://api.vk.com/method/groups.getById?group_ids={ids}&'
        'fields=type,is_closed,name,description,members_count,status,verified,site,age_limits&'
        'v={version}&access_token={token}')

    def __init__(self):
        self.response = None
        self.num = self.IDS_PER_TASK

    def build_url(self, ids, version, token):
        return self.URL_PATTERN.format(ids=ids, version=version, token=token)

    async def vk_get_communities(self, session, token):
        ids = [id for id in range(0, (self.IDS_PER_TASK))]
        version = vkapiclient.VERSION
        url = self.build_url(ids, version, token)
        self.response = await super().get_data(session, url)
        self.handle_response(self.response)

    def handle_error(self):
        errmsg = 'Unknown  error occurred'
        err = self.response.get('error')
        if err:
            errmsg = err.get('error_msg', errmsg)
            logging.error(errmsg)
            raise Exception

    def handle_response(self,resp):
        data_list = resp.get('response')
        if data_list:
            logging.info(f'data received')
            print(data_list)
        else:
            self.handle_error()
