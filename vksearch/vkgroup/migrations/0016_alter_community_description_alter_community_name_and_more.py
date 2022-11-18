# Generated by Django 4.1.3 on 2022-11-13 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vkgroup', '0015_alter_community_name_alter_community_site_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='description',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='name',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='community',
            name='site',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=512, unique=True),
        ),
    ]
