# Generated by Django 2.2.11 on 2020-04-06 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_auto_20200328_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_page_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
