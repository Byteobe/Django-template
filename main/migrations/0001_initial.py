# Generated by Django 5.0.7 on 2024-07-14 16:39

import django.contrib.gis.db.models.fields
import django.db.models.deletion
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre de País')),
                ('iso_code', models.CharField(max_length=3, unique=True, verbose_name='ISO Code')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name')),
            ],
            options={
                'verbose_name': 'País',
                'verbose_name_plural': 'Paises',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Configuración',
                'verbose_name_plural': 'Configuraciones',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre del Departamento')),
                ('dane_code', models.CharField(max_length=3, verbose_name='Código DANE')),
                ('geonames_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Código GeoNames')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='states', to='main.country')),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre del Municipio')),
                ('dane_code', models.CharField(max_length=3, verbose_name='Código DANE')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name')),
                ('coords_lat', models.FloatField(blank=True, null=True)),
                ('coords_long', models.FloatField(blank=True, null=True)),
                ('geo_location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='main.state', verbose_name='Municipios')),
            ],
            options={
                'verbose_name': 'Municipios',
                'verbose_name_plural': 'Municipios',
                'ordering': ('name',),
            },
        ),
    ]
