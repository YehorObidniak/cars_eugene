# Generated by Django 4.1.7 on 2023-04-24 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_brands_id_alter_brands_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_any',
            name='post_created_at',
            field=models.IntegerField(default=1682336949.835862),
        ),
    ]