# Generated by Django 4.1.2 on 2022-11-01 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vkgroup", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="community",
            name="description",
            field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="community",
            name="members",
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name="communitytype",
            name="name",
            field=models.TextField(null=True, unique=True),
        ),
    ]
