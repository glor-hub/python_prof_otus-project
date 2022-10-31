# Generated by Django 4.1.2 on 2022-11-01 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CommunityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('vk_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('deactivated', models.BooleanField(default=False)),
                ('description', models.TextField(default=None)),
                ('verified', models.BooleanField(null=True)),
                ('name', models.CharField(max_length=64)),
                ('site', models.CharField(max_length=128)),
                ('members', models.PositiveIntegerField(blank=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vkgroup.communitytype')),
            ],
        ),
    ]
