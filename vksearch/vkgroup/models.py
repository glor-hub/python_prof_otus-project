from django.db import models

# from vk_services import get_data_from_vk


# Create your models here.
class Community(models.Model):
    vk_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    site = models.CharField(max_length=128)
    members = models.PositiveIntegerField()
    # age_limits=
    description = models.TextField(blank=True)
    site = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        post_data = {'remote_api_file_field': self.file}
        get_data_from_vk()
        requests.post(REMOTE_API_URL, data=post_data)
        super(Community).save()


class Audience(models.Model):
    # community = models.ForeignKey(Community)
    # selector = models.ForeignKey(Selector, db_column='profile_id')
    count = models.IntegerField()
