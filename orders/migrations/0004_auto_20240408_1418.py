# Generated by Django 3.1 on 2024-04-08 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20240408_1349'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='is_ordered',
            new_name='ordered',
        ),
    ]