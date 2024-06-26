# Generated by Django 4.2.6 on 2023-11-03 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id_rol', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_rol', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id_persona', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('apellido_paterno', models.CharField(max_length=255)),
                ('apellido_materno', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=15)),
                ('correo', models.EmailField(max_length=254)),
                ('contrasena', models.CharField(max_length=255)),
                ('id_rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen_app.rol')),
            ],
        ),
    ]
