# Generated by Django 3.0.5 on 2020-04-16 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0029_auto_20200416_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussiongroup',
            name='group_image',
            field=models.ImageField(default='images/group_pictures/no_img.jpg', max_length=1000, upload_to='images/group_pictures/'),
        ),
        migrations.AlterField(
            model_name='readinggroup',
            name='group_image',
            field=models.ImageField(default='images/group_pictures/no_img.jpg', max_length=1000, upload_to='images/group_pictures/'),
        ),
        migrations.AlterField(
            model_name='recommendationgroup',
            name='group_image',
            field=models.ImageField(default='images/group_pictures/no_img.jpg', max_length=1000, upload_to='images/group_pictures/'),
        ),
    ]
