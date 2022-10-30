from . import vkapiclient
from .base_task import BaseTask

class CommunityTask(BaseTask):
    IDS_PER_TASK = 5
    URL_PATTERN = (
        'https://api.vk.com/method/groups.getById?group_ids={ids}&'
        'fields=type,is_closed,name,description,members_count,status,verified,site,age_limits&'
        'v={version}&access_token={token}')

    def __init__(self):
        self.num = self.IDS_PER_TASK

    def build_url(self, ids, version, token):
        return self.URL_PATTERN.format(ids=ids, version=version, token=token)

    async def vk_get_communities(self, session, token):
        ids = [id for id in range(1, (self.IDS_PER_TASK + 1))]
        version = vkapiclient.VERSION
        url = self.build_url(ids, version,token)
        data = await super().get_data(session,url)
        print(data)
