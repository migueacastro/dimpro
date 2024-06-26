# Generated by Django 5.0.1 on 2024-02-23 16:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dimpro', '0027_alter_order_client_id_alter_order_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='client_id',
            field=models.ForeignKey(on_delete=models.SET('Deleted User'), related_name='orders', to='dimpro.contact'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user_email',
            field=models.ForeignKey(on_delete=models.SET('Deleted User'), related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
    ]
