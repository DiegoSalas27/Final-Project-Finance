# Generated by Django 2.1.1 on 2018-10-24 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leasing', '0025_auto_20181023_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestamo',
            name='periodo_inicial_pg',
            field=models.IntegerField(default=0),
        ),
    ]
