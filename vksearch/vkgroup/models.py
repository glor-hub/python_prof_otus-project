from django.db import models


class CommunityType(models.Model):
    GROUPS_TYPES = [
        ('GROUP', 'group'),
        ('PAGE', 'page'),
        ('EVENT', 'event')
    ]
    data = [
        {'type': 'group'},
        {'type': 'page'},
        {'type': 'event'}
    ]
    name = models.TextField(choices=GROUPS_TYPES, default='GROUP', unique=True)
    objects = models.Manager()

    @classmethod
    def create_table_with_data(cls):
        type_instances = []
        for d in cls.data:
            type_instances.append(
                CommunityType(name=d['type'])
            )
        CommunityType.objects.bulk_create(type_instances)


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
    deactivated = models.BooleanField()
    age_vk = models.PositiveIntegerField(choices=AGE_VK_TYPES, null=True)
    description = models.TextField(null=True)
    verified = models.BooleanField(null=True)
    name = models.TextField(null=True)
    site = models.TextField(null=True)
    members = models.PositiveIntegerField(blank=True, null=True)
    status = models.TextField(null=True)
    is_updated = models.DateTimeField(auto_created=False, auto_now_add=True)

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
    AGE_16_YOUNGER = 2
    AGE_16_18 = 3
    AGE_18_24 = 4
    AGE_25_29 = 5
    AGE_30_34 = 6
    AGE_35_44 = 7
    AGE_45_54 = 8
    AGE_55_64 = 9
    AGE_65_OLDER = 10

    AGES_RANGE = [
        (AGE_UNKNOWN, 'ALL'),
        (AGE_16_YOUNGER, '16-'),
        (AGE_16_18, '16-18'),
        (AGE_18_24, '18-24'),
        (AGE_25_29, '25-29'),
        (AGE_30_34, '30-34'),
        (AGE_35_44, '35-44'),
        (AGE_45_54, '45-54'),
        (AGE_55_64, '55-64'),
        (AGE_65_OLDER, '65+')
    ]
    data = [
        {'age': AGE_UNKNOWN},
        {'age': AGE_16_YOUNGER},
        {'age': AGE_16_18},
        {'age': AGE_18_24},
        {'age': AGE_25_29},
        {'age': AGE_30_34},
        {'age': AGE_35_44},
        {'age': AGE_45_54},
        {'age': AGE_55_64},
        {'age': AGE_65_OLDER}
    ]
    range = models.PositiveIntegerField(choices=AGES_RANGE, default=AGE_UNKNOWN, unique=True)
    objects = models.Manager()

    @classmethod
    def create_table_with_data(cls):
        age_instances = []
        for datum in cls.data:
            age_instances.append(
                AgeRange(range=datum['age'])
            )
        AgeRange.objects.bulk_create(age_instances)

    def __str__(self):
        return f'age range: {self.range}'


class Country(models.Model):
    UNKNOWN_COUNTRY = 'Неизвестная страна'
    name = models.TextField(unique=True, null=False)
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
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=False, default=1)
    age_range = models.ForeignKey('AgeRange', on_delete=models.CASCADE, null=False, default=1)
    sex = models.SmallIntegerField(choices=SEX_CHOICES, default=SEX_UNKNOWN)
    objects = models.Manager()

    class Meta:
        unique_together = ('country', 'age_range', 'sex')


class Audience(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=False, default=1)
    profile = models.ForeignKey(AudienceProfile, on_delete=models.CASCADE, null=False, default=1)
    count = models.IntegerField(default=0)
    objects = models.Manager()

    class Meta:
        unique_together = ('community', 'profile')

    def __str__(self):
        return (f'audience id:{self.pk} of community {self.community.name}')
