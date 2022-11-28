# Generated by Django 4.1.2 on 2022-11-01 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "vkgroup",
            "0002_alter_community_description_alter_community_members_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="community",
            name="type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="vkgroup.communitytype",
            ),
        ),
        migrations.AlterField(
            model_name="communitytype",
            name="name",
            field=models.TextField(db_index=True, unique=True),
        ),
    ]
