# Generated by Django 2.1.1 on 2018-10-25 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leasing', '0039_auto_20181024_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='periodo_cap',
            field=models.IntegerField(choices=[(0, 'Ninguna'), (360, 'Diaria'), (24, 'Quincenal'), (12, 'Mensual'), (6, 'Bimestral'), (4, 'Trimestral'), (3, 'Cuatrimestral'), (2, 'Semestral'), (1, 'Anual')], default=360),
        ),
    ]
