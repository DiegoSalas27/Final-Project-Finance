# Generated by Django 2.1.1 on 2018-10-25 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leasing', '0036_auto_20181024_2154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prestamo',
            name='periodo_cap',
        ),
    ]
