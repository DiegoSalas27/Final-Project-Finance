# Generated by Django 2.1.1 on 2018-10-25 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leasing', '0034_auto_20181024_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='periodo_cap',
            field=models.CharField(choices=[(1, 'Diaria'), (15, 'Quincenal'), (30, 'Mensual')], max_length=20),
        ),
    ]
