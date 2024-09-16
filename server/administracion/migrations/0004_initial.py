# Generated by Django 5.1.1 on 2024-09-16 09:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Propietario',
            fields=[
                ('dni', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=15)),
                ('direccion', models.CharField(max_length=50)),
                ('tipo_propietarario', models.CharField(choices=[('PF', 'Persona Fisica'), ('PJ', 'Persona Juridica')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Administracion',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id_administracion', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('num_receptor', models.IntegerField(unique=True)),
                ('nombre_comercial', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=50)),
                ('localidad', models.CharField(max_length=20)),
                ('provincia', models.CharField(max_length=20)),
                ('numero_admon', models.IntegerField()),
                ('codigo_postal', models.IntegerField(null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.CharField(max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.propietario')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]