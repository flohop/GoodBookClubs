# Generated by Django 2.2.11 on 2020-03-22 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0007_auto_20200322_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussiongroup',
            name='group_members',
            field=models.ManyToManyField(blank=True, related_name='discussion_group_members', to='account.Profile'),
        ),
    ]
