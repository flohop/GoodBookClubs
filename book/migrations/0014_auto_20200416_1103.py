# Generated by Django 3.0.5 on 2020-04-16 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0013_auto_20200409_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_cover_image',
            field=models.ImageField(default='book_covers/no_cover.png', upload_to='book_covers/'),
        ),
    ]
