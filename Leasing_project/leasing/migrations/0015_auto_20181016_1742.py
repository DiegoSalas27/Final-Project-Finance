# Generated by Django 2.1.1 on 2018-10-16 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leasing', '0014_auto_20181016_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestamo',
            name='TCEA',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='prestamo',
            name='VAN',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='prestamo',
            name='cuotas',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='intereses',
            field=models.FloatField(null=True),
        ),
    ]
