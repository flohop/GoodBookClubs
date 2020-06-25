# Generated by Django 3.0.5 on 2020-04-16 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0031_auto_20200416_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussiongroup',
            name='group_image',
            field=models.ImageField(default='images/group_pictures/no_img.jpg', max_length=1000, upload_to='images/group_pictures/'),
        ),
        migrations.AlterField(
            model_name='discussiongroup',
            name='is_private_group',
            field=models.BooleanField(default=False, max_length=255),
        ),
        migrations.AlterField(
            model_name='discussiongroup',
            name='slug',
            field=models.SlugField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='readinggroup',
            name='group_image',
            field=models.ImageField(default='images/group_pictures/no_img.jpg', max_length=1000, upload_to='images/group_pictures/'),
        ),
        migrations.AlterField(
            model_name='readinggroup',
            name='is_private_group',
            field=models.BooleanField(default=False, max_length=255),
        ),
        migrations.AlterField(
            model_name='readinggroup',
            name='slug',
            field=models.SlugField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='recommendationgroup',
            name='group_image',
            field=models.ImageField(default='images/group_pictures/no_img.jpg', max_length=1000, upload_to='images/group_pictures/'),
        ),
        migrations.AlterField(
            model_name='recommendationgroup',
            name='is_private_group',
            field=models.BooleanField(default=False, max_length=255),
        ),
        migrations.AlterField(
            model_name='recommendationgroup',
            name='slug',
            field=models.SlugField(blank=True, max_length=500),
        ),
    ]