# Generated by Django 2.2.11 on 2020-03-22 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0008_auto_20200322_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussiongroup',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='readinggroup',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='recommendationgroup',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
