# Generated by Django 3.0.5 on 2020-04-17 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0034_auto_20200417_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readinggroup',
            name='current_book_current_page',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]