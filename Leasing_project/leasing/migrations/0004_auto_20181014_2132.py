# Generated by Django 2.1.1 on 2018-10-15 02:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leasing', '0003_auto_20181014_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
