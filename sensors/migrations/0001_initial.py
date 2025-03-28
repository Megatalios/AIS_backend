# Generated by Django 5.1.6 on 2025-03-01 20:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cars', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('engine_rpm', models.FloatField()),
                ('intake_air_temperature', models.FloatField()),
                ('mass_air_flow_sensor', models.FloatField(blank=True, null=True)),
                ('injection_duration', models.FloatField(blank=True, null=True)),
                ('throttle_position', models.FloatField(blank=True, null=True)),
                ('vehicle_speed', models.FloatField(blank=True, null=True)),
                ('manifold_absolute_pressure', models.FloatField(blank=True, null=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensor_data', to='cars.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensor_data', to='users.user')),
            ],
        ),
    ]
