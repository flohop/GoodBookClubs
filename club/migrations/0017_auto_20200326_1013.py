# Generated by Django 2.2.11 on 2020-03-26 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0016_auto_20200325_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussiongroup',
            name='current_book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='book.Book'),
        ),
        migrations.AlterField(
            model_name='discussiongroup',
            name='group_creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='discussion_group_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='readinggroup',
            name='current_book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reading_group_book', to='book.Book'),
        ),
        migrations.AlterField(
            model_name='readinggroup',
            name='group_creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reading_group_creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
