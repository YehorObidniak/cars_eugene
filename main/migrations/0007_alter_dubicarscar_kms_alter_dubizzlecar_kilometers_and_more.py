# Generated by Django 4.1.7 on 2023-02-18 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_dubizzlecar_price_alter_yallamotorcar_kms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dubicarscar',
            name='kms',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='dubizzlecar',
            name='kilometers',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='yallamotorcar',
            name='price',
            field=models.IntegerField(),
        ),
    ]