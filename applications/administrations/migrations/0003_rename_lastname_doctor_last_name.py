# Generated by Django 4.2 on 2023-07-26 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrations', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='lastname',
            new_name='last_name',
        ),
    ]
