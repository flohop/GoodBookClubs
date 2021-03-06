# Generated by Django 2.2.11 on 2020-03-21 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussiongroup',
            name='group_members',
            field=models.ManyToManyField(related_name='club_discussiongroup_group_members', to='club.Profile'),
        ),
        migrations.AlterField(
            model_name='readinggroup',
            name='group_members',
            field=models.ManyToManyField(related_name='club_readinggroup_group_members', to='club.Profile'),
        ),
    ]
