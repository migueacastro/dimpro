# Generated by Django 5.0.1 on 2024-02-04 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dimpro', '0005_alter_product_reference'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlegraUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=128)),
                ('token', models.CharField(max_length=256)),
            ],
        ),
    ]
