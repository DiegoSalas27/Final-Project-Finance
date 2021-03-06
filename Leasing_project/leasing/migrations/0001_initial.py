# Generated by Django 2.1.1 on 2018-10-14 19:12

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio_venta', models.DecimalField(decimal_places=4, max_digits=11)),
                ('cuota_inicial', models.DecimalField(decimal_places=4, max_digits=11)),
                ('empresa_ofertante', models.CharField(max_length=100)),
                ('tipo_de_pago', models.CharField(max_length=10)),
                ('plazos_de_pago', models.IntegerField()),
                ('tipo_tasa_interes', models.CharField(max_length=100)),
                ('TEA', models.DecimalField(decimal_places=4, max_digits=7)),
                ('comision_rt', models.DecimalField(decimal_places=4, max_digits=9)),
                ('fotocopias', models.DecimalField(decimal_places=4, max_digits=9)),
                ('gastos_admin', models.DecimalField(decimal_places=4, max_digits=9)),
                ('fecha_inicio', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('seguro_riesgo', models.DecimalField(decimal_places=4, max_digits=7)),
                ('seguro_desgravamen', models.DecimalField(decimal_places=4, max_digits=7)),
                ('plazo_de_gracia', models.IntegerField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
