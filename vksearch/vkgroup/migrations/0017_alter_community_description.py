# Generated by Django 4.1.3 on 2022-11-13 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vkgroup', '0016_alter_community_description_alter_community_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='description',
            field=models.CharField(max_length=512, null=True),
        ),
    ]
