# Generated by Django 4.2.11 on 2024-06-02 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_SellsSubs', '0007_rename_ciudad_compra_municipio'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='total_pagar',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
