# Generated by Django 4.1.3 on 2022-11-21 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("vkgroup", "0024_alter_audience_community_alter_audience_profile_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="community", old_name="is_updated", new_name="update_at",
        ),
    ]
