# Generated by Django 4.2.6 on 2023-11-28 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('almacen_app', '0002_alter_rol_nombre_rol'),
    ]

    operations = [
        migrations.CreateModel(
            name='Almacen',
            fields=[
                ('id_almacen', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_almacen', models.CharField(max_length=255)),
                ('direccion', models.TextField()),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_producto', models.CharField(max_length=255)),
                ('cantidad', models.IntegerField()),
            ],
        ),
    ]
