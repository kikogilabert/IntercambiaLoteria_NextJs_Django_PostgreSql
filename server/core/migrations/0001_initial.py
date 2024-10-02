# Generated by Django 5.1.1 on 2024-10-01 15:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=2, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ComunidadAutonoma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=2, unique=True)),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comunidades_autonomas', to='core.pais')),
            ],
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=2, unique=True)),
                ('comunidad_autonoma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='provincias', to='core.comunidadautonoma')),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provincias', to='core.pais')),
            ],
        ),
    ]
