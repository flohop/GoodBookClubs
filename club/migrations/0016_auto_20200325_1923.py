# Generated by Django 2.2.11 on 2020-03-25 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0015_auto_20200325_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussiongroup',
            name='group_description',
            field=models.CharField(default='Group Description', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='readinggroup',
            name='group_description',
            field=models.CharField(default='Group Description', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recommendationgroup',
            name='group_description',
            field=models.CharField(default='Group Description', max_length=500),
            preserve_default=False,
        ),
    ]