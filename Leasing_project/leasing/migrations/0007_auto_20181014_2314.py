# Generated by Django 2.1.1 on 2018-10-15 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leasing', '0006_auto_20181014_2228'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prestamo',
            old_name='Intereses',
            new_name='intereses',
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='cuotas',
            field=models.IntegerField(null=True),
        ),
    ]
