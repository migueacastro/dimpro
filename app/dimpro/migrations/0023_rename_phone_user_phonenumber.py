# Generated by Django 5.0.1 on 2024-02-18 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dimpro', '0022_alter_user_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phone',
            new_name='phonenumber',
        ),
    ]
