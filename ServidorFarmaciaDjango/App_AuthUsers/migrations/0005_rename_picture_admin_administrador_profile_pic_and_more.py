# Generated by Django 4.2.11 on 2024-05-05 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_AuthUsers', '0004_rename_farm_emp_empleado_farmacia_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='administrador',
            old_name='picture_admin',
            new_name='profile_pic',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='picture_cli',
            new_name='profile_pic',
        ),
        migrations.RenameField(
            model_name='empleado',
            old_name='picture_emp',
            new_name='profile_pic',
        ),
        migrations.RenameField(
            model_name='gerente',
            old_name='picture_admin',
            new_name='profile_pic',
        ),
    ]
