# Generated by Django 5.0.1 on 2024-02-25 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dimpro', '0030_contact_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order_product',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
    ]
