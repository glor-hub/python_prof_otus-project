# Generated by Django 4.1.3 on 2022-11-15 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("vkgroup", "0020_alter_country_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="community",
            old_name="update",
            new_name="is_updated",
        ),
    ]
