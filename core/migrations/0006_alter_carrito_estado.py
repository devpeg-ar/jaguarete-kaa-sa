# Generated by Django 3.2.4 on 2021-07-04 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_carrito_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrito',
            name='estado',
            field=models.BooleanField(default=False),
        ),
    ]
