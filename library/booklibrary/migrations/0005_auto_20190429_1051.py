# Generated by Django 2.2 on 2019-04-29 02:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booklibrary', '0004_auto_20190429_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='date_borrow',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 29, 10, 51, 29, 198934)),
        ),
        migrations.AlterField(
            model_name='history',
            name='date_return',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 29, 10, 51, 29, 198934)),
        ),
    ]
