# Generated by Django 2.0.2 on 2018-02-20 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('active', models.BooleanField()),
                ('approved', models.BooleanField()),
                ('authorized_members', models.IntegerField()),
                ('badge_image', models.URLField()),
                ('contact_email', models.EmailField(max_length=200)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_label', models.CharField(max_length=50)),
                ('info_url', models.URLField()),
                ('is_academic_or_nonprofit', models.BooleanField()),
                ('is_study', models.BooleanField()),
                ('leader', models.CharField(max_length=50)),
                ('long_description', models.TextField()),
                ('name', models.CharField(max_length=50)),
                ('organization', models.CharField(max_length=200)),
                ('request_message_permission', models.BooleanField()),
                ('request_sources_access', models.CharField(max_length=100)),
                ('request_username_access', models.BooleanField()),
                ('returned_data_description', models.CharField(max_length=200)),
                ('short_description', models.TextField()),
                ('slug', models.SlugField()),
                ('type', models.CharField(max_length=50)),
            ],
        ),
    ]
