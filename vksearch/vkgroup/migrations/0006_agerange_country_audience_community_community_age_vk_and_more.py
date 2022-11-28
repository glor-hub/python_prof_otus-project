# Generated by Django 4.1.3 on 2022-11-12 12:25

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vkgroup", "0005_alter_community_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="AgeRange",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "range",
                    models.PositiveIntegerField(
                        choices=[
                            (1, "ALL"),
                            (2, "16-18"),
                            (3, "18-24"),
                            (4, "24-30"),
                            (5, "30-35"),
                            (6, "35-45"),
                            (7, "45-55"),
                            (8, "55-65"),
                            (9, "65+"),
                        ],
                        default=1,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="audience",
            name="community",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="vkgroup.community",
            ),
        ),
        migrations.AddField(
            model_name="community",
            name="age_vk",
            field=models.PositiveIntegerField(
                choices=[(1, "0+"), (2, "16+"), (3, "18+")], default=1, unique=True
            ),
        ),
        migrations.AddField(
            model_name="community",
            name="status",
            field=models.CharField(default="", max_length=64),
        ),
        migrations.AddField(
            model_name="community",
            name="update",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="communitytype",
            name="name",
            field=models.TextField(
                choices=[("GROUP", "group"), ("PAGE", "page"), ("EVENT", "event")],
                default="GROUP",
                unique=True,
            ),
        ),
        migrations.CreateModel(
            name="AudienceProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sex",
                    models.SmallIntegerField(
                        choices=[(0, "UNKNOWN"), (1, "Female"), (2, "Male")]
                    ),
                ),
                (
                    "age_range",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vkgroup.agerange",
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vkgroup.country",
                    ),
                ),
            ],
            options={
                "unique_together": {("country", "age_range", "sex")},
            },
        ),
        migrations.AddField(
            model_name="audience",
            name="profile",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="vkgroup.audienceprofile",
            ),
        ),
    ]
