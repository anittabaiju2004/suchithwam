# Generated by Django 5.1.3 on 2025-03-11 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_register',
            name='latitude',
            field=models.DecimalField(decimal_places=7, default=0.0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='tbl_register',
            name='longitude',
            field=models.DecimalField(decimal_places=7, default=0.0, max_digits=20),
        ),
    ]
