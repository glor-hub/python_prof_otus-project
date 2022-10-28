from django.db import models


# Create your models here.
class Community(models.Model):
    vk_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    site = models.CharField(max_length=128)
    members=models.PositiveIntegerField()
    age_limits=
    description = models.TextField(blank=True)
    site= models.CharField(max_length=128)

class Audience(models.Model):
    community = models.ForeignKey(Community, db_column='community_vkid')
    selector = models.ForeignKey(Selector, db_column='profile_id')
    count = models.IntegerField()
