# Generated by Django 5.0.1 on 2024-02-16 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dimpro', '0018_user_phone_alter_order_client_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_operator',
            field=models.BooleanField(default=False),
        ),
    ]
