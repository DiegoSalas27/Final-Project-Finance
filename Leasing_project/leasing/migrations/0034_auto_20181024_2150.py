# Generated by Django 2.1.1 on 2018-10-25 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leasing', '0033_auto_20181024_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='periodo_cap',
            field=models.CharField(choices=[(1, 'Diaria'), (15, 'Quincenal'), (30, 'Mensual'), (60, 'Bimestral'), (90, 'Trimestral'), (120, 'Cuatrimestral'), (180, 'Semestral'), (360, 'Anual')], default=1, max_length=20),
        ),
    ]
