# Generated by Django 5.0.1 on 2024-02-06 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dimpro', '0013_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='item',
            field=models.CharField(max_length=64),
        ),
    ]
