# Generated by Django 4.1.7 on 2023-03-01 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_brands_name_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='regSpecs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
            ],
        ),
        migrations.DeleteModel(
            name='Models',
        ),
    ]