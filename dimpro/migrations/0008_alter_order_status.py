# Generated by Django 5.0.1 on 2024-02-04 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dimpro', '0007_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[('preparado', 'Preparado'), ('pendiente', 'Pendiente')]),
        ),
    ]