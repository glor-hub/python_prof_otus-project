from django.db import models

class CommunityType(models.Model):
    name = models.TextField(unique=True)
    objects = models.Manager()

class Community(models.Model):
    AGES = [
        (1, '0+'),
        (2, '16+'),
        (3, '18+')
        ]
    vk_id = models.PositiveIntegerField(primary_key=True, null=False)
    type = models.ForeignKey('CommunityType', on_delete=models.CASCADE, null=True)
    deactivated = models.BooleanField(default=False)
    age_limits=models.PositiveIntegerField(choices=AGES, default=1,unique=True )
    description = models.TextField(default='', null=True)
    verified = models.BooleanField(null=True)
    name = models.CharField(max_length=64)
    site = models.CharField(max_length=128)
    members = models.PositiveIntegerField(blank=True, default=0)
    status = models.CharField(max_length=64)

    objects = models.Manager()
    # def save(self, *args, **kwargs):
    #     post_data = {'remote_api_file_field': self.file}
    #     get_data_from_vk()
    #     requests.post(REMOTE_API_URL, data=post_data)
    #     super(Community).save()
    def __str__(self):
        return (f'community: {self.name} id: {vk_id}')

class Age(models.Model):
    AGES_RANGE = [
        (1, 'ALL'),
        (2, '16-18'),
        (3, '18-24'),
        (4, '24-30'),
        (5, '30-35'),
        (6, '35-45'),
        (7, '45-55'),
        (8, '55-65'),
        (9, '65+')
    ]
    range = models.PositiveIntegerField(choices=AGES_RANGE, default=1, unique=True)

    def __str__(self):
        return f('age range: {self.range}')


class Country(models.Model):
    name = models.TextField(unique=True)
    objects = models.Manager()
# method: database.getCountriesById
    def __str__(self):
        return self.name

class AudienceProfile(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True)
    users_age=models.ForeignKey('Age', on_delete=models.CASCADE, null=True)
    class Meta:
        unique_together = (('country', 'question'),)


class Audience(models.Model):
    community = models.ForeignKey(Community,  on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(AudienceProfile,  on_delete=models.CASCADE, null=True)
    count = models.IntegerField()
    def __str__(self):
        return (f'audience id:{pk} of {community.name} ')