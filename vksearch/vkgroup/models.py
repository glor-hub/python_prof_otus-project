from django.db import models


# age_limit = models.SmallIntegerField(blank=True, null=True)
# updated = models.DateTimeField()
# audience_updated = models.DateTimeField()
# IKE = 'L'
# DISLIKE = 'D'
# NONE = 'N'
# STATUS = [
#     (LIKE, 'Like'),
#     (DISLIKE, 'Dislike'),
#     (NONE, 'None')
# ]
class CommunityType(models.Model):
    name = models.TextField(unique=True)

    objects = models.Manager()


# Create your models here.
class Community(models.Model):
    vk_id = models.PositiveIntegerField(primary_key=True, null=False)
    type = models.ForeignKey('CommunityType', on_delete=models.CASCADE, null=True)
    deactivated = models.BooleanField(default=False)
    description = models.TextField(default='', null=True)
    verified = models.BooleanField(null=True)
    name = models.CharField(max_length=64)
    site = models.CharField(max_length=128)
    members = models.PositiveIntegerField(blank=True, default=0)
    # age_limits=
    objects = models.Manager()
    # def save(self, *args, **kwargs):
    #     post_data = {'remote_api_file_field': self.file}
    #     get_data_from_vk()
    #     requests.post(REMOTE_API_URL, data=post_data)
    #     super(Community).save()


class Audience(models.Model):
    # community = models.ForeignKey(Community)
    # selector = models.ForeignKey(Selector, db_column='profile_id')
    count = models.IntegerField()
