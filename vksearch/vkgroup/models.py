from django.db import models


class CommunityType(models.Model):
    GROUPS_TYPES = [
        ('GROUP', 'group'),
        ('PAGE', 'page'),
        ('EVENT', 'event')
    ]
    name = models.TextField(choices=GROUPS_TYPES, default='GROUP',unique=True)
    objects = models.Manager()


class Community(models.Model):
    AGE_UNKNOWN = 1
    AGE_16_OLDER = 2
    AGE_18_OLDER = 3
    AGE_VK_TYPES = [
        (1, '0+'),
        (2, '16+'),
        (3, '18+')
    ]
    vk_id = models.PositiveIntegerField(primary_key=True, null=False)
    type = models.ForeignKey('CommunityType', on_delete=models.CASCADE, null=True)
    deactivated = models.BooleanField(default=False)
    age_vk = models.PositiveIntegerField(choices=AGE_VK_TYPES, null=True)
    description = models.TextField(default='', null=True)
    verified = models.BooleanField(null=True)
    name = models.CharField(max_length=64)
    site = models.CharField(max_length=128, null=True)
    members = models.PositiveIntegerField(blank=True,null=True)
    status = models.CharField(max_length=64, null=True)
    update=models.DateTimeField(auto_created=False, auto_now_add=True)

    objects = models.Manager()

    # def save(self, *args, **kwargs):
    #     post_data = {'remote_api_file_field': self.file}
    #     get_data_from_vk()
    #     requests.post(REMOTE_API_URL, data=post_data)
    #     super(Community).save()
    def __str__(self):
        return (f'community: {self.name} id: {self.vk_id}')


class AgeRange(models.Model):
    AGE_UNKNOWN = 1
    AGE_16_18 = 2
    AGE_18_24 = 3
    AGE_24_30 = 4
    AGE_30_35 = 5
    AGE_35_45 = 6
    AGE_45_55 = 7
    AGE_55_65 = 8
    AGE_65_OLDER = 9

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
    range = models.PositiveIntegerField(choices=AGES_RANGE, default=AGE_UNKNOWN, unique=True)

    def __str__(self):
        return f'age range: {self.range}'


class Country(models.Model):
    name = models.TextField(unique=True)
    objects = models.Manager()

    # method: database.getCountriesById
    def __str__(self):
        return self.name


class AudienceProfile(models.Model):
    SEX_UNKNOWN = 0
    SEX_FEMALE = 1
    SEX_MALE = 2
    SEX_CHOICES = (
        (SEX_UNKNOWN, 'UNKNOWN'),
        (SEX_FEMALE, 'Female'),
        (SEX_MALE, 'Male')
    )
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True)
    age_range = models.ForeignKey('AgeRange', on_delete=models.CASCADE, null=True)
    sex = models.SmallIntegerField(choices=SEX_CHOICES, default=SEX_UNKNOWN)

    class Meta:
        unique_together = ('country', 'age_range', 'sex')


class Audience(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(AudienceProfile, on_delete=models.CASCADE, null=True)
    count = models.IntegerField()

    def __str__(self):
        return (f'audience id:{self.pk} of community {self.community.name} ')
