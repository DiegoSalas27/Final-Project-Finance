# Generated by Django 2.1.1 on 2018-10-25 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leasing', '0028_prestamo_periodo_cap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='periodo_cap',
            field=models.CharField(choices=[(360, 'Diaria'), (24, 'Quincenal'), (12, 'Mensual'), (6, 'Bimestral'), (4, 'Trimestral'), (3, 'Cuatrimestral'), (2, 'Semestral'), (1, 'Anual')], default=1, max_length=20),
        ),
    ]
