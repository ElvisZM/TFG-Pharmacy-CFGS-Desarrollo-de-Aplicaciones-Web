# Generated by Django 4.2.11 on 2024-06-03 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('App_SellsSubs', '0001_initial'),
        ('App_ProductProvider', '0001_initial'),
        ('App_AuthUsers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='votacion_prod',
            field=models.ManyToManyField(related_name='votacion_prod', through='App_SellsSubs.Votacion', to='App_ProductProvider.producto'),
        ),
        migrations.AddField(
            model_name='administrador',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
