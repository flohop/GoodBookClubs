# Generated by Django 3.0.5 on 2020-04-16 11:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0020_auto_20200416_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_release_year',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2020)]),
        ),
    ]
