# Generated by Django 2.1.1 on 2018-10-15 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leasing', '0005_empresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='telefono',
            field=models.IntegerField(),
        ),
    ]
