# Generated by Django 5.0.6 on 2024-06-06 01:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_token'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Token',
            new_name='TokenStore',
        ),
    ]
