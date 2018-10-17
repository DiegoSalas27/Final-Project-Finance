# Generated by Django 2.1.1 on 2018-10-16 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leasing', '0013_auto_20181016_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='TEA',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='comision_de_activacion',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='comision_de_estudio',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='comision_periodica',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='costos_notariales',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='costos_registrales',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='recompra',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='seguro_riesgo',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='tasacion',
            field=models.FloatField(null=True),
        ),
    ]