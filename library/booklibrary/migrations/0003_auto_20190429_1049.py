# Generated by Django 2.2 on 2019-04-29 02:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booklibrary', '0002_auto_20190429_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='date_borrow',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 29, 10, 49, 22, 961866)),
        ),
        migrations.AlterField(
            model_name='history',
            name='date_return',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 29, 10, 49, 22, 961866)),
        ),
    ]
