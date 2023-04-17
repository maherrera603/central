# Generated by Django 4.2 on 2023-04-16 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cites', '0001_initial'),
        ('pattients', '0001_initial'),
        ('administrations', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cites',
            name='id_pattient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pattients.pattient'),
        ),
        migrations.AddField(
            model_name='cites',
            name='id_speciality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrations.speciality'),
        ),
        migrations.AddField(
            model_name='cites',
            name='id_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrations.status'),
        ),
    ]