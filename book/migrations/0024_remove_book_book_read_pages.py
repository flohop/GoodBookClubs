# Generated by Django 3.0.5 on 2020-04-17 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0023_auto_20200416_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book_read_pages',
        ),
    ]