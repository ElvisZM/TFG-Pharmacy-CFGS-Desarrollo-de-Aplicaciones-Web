# Generated by Django 4.2.11 on 2024-06-05 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_AuthUsers', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='administrador',
            name='source',
            field=models.CharField(default='app', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cliente',
            name='source',
            field=models.CharField(default='app', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empleado',
            name='source',
            field=models.CharField(default='app', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gerente',
            name='source',
            field=models.CharField(default='app', max_length=50),
            preserve_default=False,
        ),
    ]
