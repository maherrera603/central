# Generated by Django 4.2 on 2023-07-24 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pattients', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='family',
            old_name='id_pattient',
            new_name='pattient',
        ),
    ]
