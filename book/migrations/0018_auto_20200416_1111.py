# Generated by Django 3.0.5 on 2020-04-16 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0017_auto_20200416_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_cover_image',
            field=models.ImageField(default='book_covers/no_cover.png', max_length=1000, upload_to='book_covers/'),
        ),
        migrations.AlterField(
            model_name='book',
            name='slug',
            field=models.SlugField(blank=True, max_length=255),
        ),
    ]
